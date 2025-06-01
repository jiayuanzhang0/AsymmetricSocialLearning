# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:04:58 2023

@author: jyzhang
"""

import numpy as np
import random
import networkx as nx
import pickle
from multiprocessing import Pool, cpu_count

import os
import sys
sys.path.append('../')
import Dir
import genG


caseName_existed_list = []
with open("existedCaseName.txt", "r") as f:
    for line in f:
        caseName_existed_list.append(line.strip())


# initialization
#---------------
def set_init_strategy(G, a_initC):
    a_initD = 1-a_initC
    
    # randomly assign strategy
    strategy_list = np.zeros(len(G), dtype=int)
    strategy_list[: round(len(G)*a_initD) ]=1
    # print(strategy_list)
    random.shuffle(strategy_list)  # shuffle the array randomly
    strategy_list = list(strategy_list)
    # print(strategies)
    
    strategy_dict = dict(zip(G.nodes, strategy_list))
    nx.set_node_attributes(G, strategy_dict, 'strategy')
    # print(G.nodes(data=True))


def set_init_param(G, beta):
    beta_list = np.zeros(len(G))
    beta_list[:]=beta
    beta_list = list(beta_list)
    
    beta_dict = dict(zip(G.nodes, beta_list))
    nx.set_node_attributes(G, beta_dict, 'beta')
    # print(G.nodes(data=True)) 
#---------------


def play_step(G, payoff_matrix):
    Px_agents = np.zeros(len(G))
    
    for i in range(len(G)):
        # x_strategy: focal agent; y_strategy: neighbor strategy
        x_strategy = G.nodes[i]['strategy']
        y_strategy_neighbors = []
        for key_neighbor in list(G.neighbors(i)):
            y_strategy_neighbors.append(G.nodes[key_neighbor]['strategy'])
  
        # the reward of x after gaming with each neighbor
        payoff_to_each_neighbor = payoff_matrix[x_strategy, y_strategy_neighbors]
        
        Px = sum(payoff_to_each_neighbor)
        Px_agents[i] = Px        
    return Px_agents
 

def update_step(G, Px_agents, beta0, beta1):
    x_strategy_agents = np.array(list(nx.get_node_attributes(G, 'strategy').values()))
    nx.set_node_attributes(G, dict(zip(G.nodes, x_strategy_agents)), 'strategy_prev')
    
    # Set beta according to strategy
    mask_strategy0 = x_strategy_agents == 0
    x_beta_agents = np.where(mask_strategy0, beta0, beta1)
    beta_dict_updated = dict(zip(G.nodes, x_beta_agents))
    nx.set_node_attributes(G, beta_dict_updated, 'beta')
    
    chosen_neighbors = np.array([random.choice(list(G.neighbors(i))) for i in range(len(G))])
    Py_agents = Px_agents[chosen_neighbors]
    y_strategy_agents = x_strategy_agents[chosen_neighbors]
    nx.set_node_attributes(G, dict(zip(G.nodes, y_strategy_agents)), 'y_strategy_prev')
    
    p_takeover = 1 / (1 + np.exp(-x_beta_agents * (Py_agents - Px_agents)))
    is_takeover = np.random.rand(len(G)) < p_takeover
    x_strategy_agents_updated = np.where(is_takeover, y_strategy_agents, x_strategy_agents)

    strategy_dict_updated = dict(zip(G.nodes, x_strategy_agents_updated))
    nx.set_node_attributes(G, strategy_dict_updated, 'strategy')

    nx.set_node_attributes(G, dict(zip(G.nodes, chosen_neighbors)), 'y')
    nx.set_node_attributes(G, dict(zip(G.nodes, Px_agents)), 'Px')
    nx.set_node_attributes(G, dict(zip(G.nodes, Py_agents)), 'Py')
    nx.set_node_attributes(G, dict(zip(G.nodes, p_takeover)), 'p_takeover')
    nx.set_node_attributes(G, dict(zip(G.nodes, is_takeover)), 'is_takeover')

    
def get_freqCooperation(G, N):
    freq_cooperation = 1-sum(nx.get_node_attributes(G, 'strategy').values())/N
    return freq_cooperation


def play_case(params):
    # params
    #-------
    n_step = params.n_step
    max_step = params.max_step
    network_type = params.network_type
    # game_type = params.game_type
    N = params.N
    z = params.z 
    # br = params.br    
    isim = params.isim
    is_resume = params.is_resume
    is_inst = params.is_inst
    n_inst = params.n_inst
    
    payoff_matrix = params.payoff_matrix
    
    beta0 = params.beta0
    beta1 = params.beta1
    
    caseName = params.caseName
    gridEnsembleName = params.gridEnsembleName
    n_step_tail = params.n_step_tail
    
    a_initC = params.a_initC
    # igrid = params.igrid
    #-------
    
    step_freqCooperation_path = Dir.step_freqCooperation_dir+caseName+'.txt'
    G_ensembleShared_path = Dir.G_ensembleShared_dir + gridEnsembleName+'.pkl'
    G_resume_path = Dir.G_resume_dir + caseName+'.pkl'
    # print(caseName)
    
    G_inst_dir = Dir.G_inst_dir+caseName+'/'
    if is_inst:
        if not os.path.exists(G_inst_dir): os.makedirs(G_inst_dir)
    
    # initialization
    #--------------------------------------------------------------------------
    if caseName in caseName_existed_list:
        print('This case has been calculated. Skip')
        return
    
    elif (os.path.exists(step_freqCooperation_path) and os.path.exists(G_resume_path) and is_resume==1):
        print('Resume file exits. Resume the old case')
        with open(G_resume_path, 'rb') as file:
            G = pickle.load(file)
        
        step_freqCooperation_old = np.loadtxt(step_freqCooperation_path)
        len_old = len(step_freqCooperation_old)
        len_new = int(len_old+n_step)
        if len_new >= max_step+1:
            len_new = max_step+1
        
        step_freqCooperation = np.zeros( (len_new, 2) )
        step_freqCooperation[:len_old] = step_freqCooperation_old
        
        step_s = len_old
        step_e = len_new-1
 
    else: 
        print('Resume file does not exist. Initialize a new case.')
        
        if isim == 0:
            print('The first case in ensemble. Gen ensemble G')
            G = genG.gen_G(N, z, network_type)
            # save G into ensemble G file
            with open(G_ensembleShared_path, 'wb') as file:
                pickle.dump(G, file)
            print()
            
        else:
            print('The non-first case in ensemble. Load ensemble G')
            # load G from ensemble G file         
            with open(G_ensembleShared_path, 'rb') as file:
                G = pickle.load(file)
            print()
        
        set_init_strategy(G, a_initC)
        #init_time_series(G)
        set_init_param(G, beta0)
        
        if is_inst:
            # save init field
            G_inst_path = G_inst_dir + '%06d'%0+'.pkl'
            with open(G_inst_path, 'wb') as file:
                pickle.dump(G, file)
        
        step_freqCooperation = np.zeros((n_step+1, 2))
        step_freqCooperation[0, 0] = 0
        step_freqCooperation[0, 1] = get_freqCooperation(G, N)

        step_s = 1
        step_e = n_step
    #--------------------------------------------------------------------------
    
    for step in range(step_s, step_e+1):
        if step%100 == 0:
            print(step)
            
        # check convergence
        if step-n_step_tail >= 0 and step % n_step_tail == 1: 
            freqCooperation_tail = step_freqCooperation[step-n_step_tail:step, 1]
            if all(freqCooperation_tail == [0.0]*n_step_tail) or all(freqCooperation_tail==[1.0]*n_step_tail):
                # print('convergent. end step: %d'%(step-1))
                step_freqCooperation = step_freqCooperation[:step]
                break

        # print(step)    
        Px_agents = play_step(G, payoff_matrix)
        update_step(G, Px_agents, beta0, beta1)      
        step_freqCooperation[step, 0] = step
        step_freqCooperation[step, 1] = get_freqCooperation(G, N)
        
        if is_inst:
            # save inst 
            if step%n_inst == 0:
                G_inst_path = G_inst_dir + '%06d'%step + '.pkl'
                # nx.write_gpickle(G, G_inst_path)
                with open(G_inst_path, 'wb') as file:
                    pickle.dump(G, file)
            
    if step_s > step_e or step == step_s:
        print('not run any step')
        return
    else:
        np.savetxt(step_freqCooperation_path, step_freqCooperation, 
                   fmt='%d %.9f'
                   )
        # nx.write_gpickle(G, G_resume_path)
        with open(G_resume_path, 'wb') as file:
            pickle.dump(G, file)
            
    print()
 

class params_case:
    def __init__(self, network_type, N, z, br, beta0, beta1, a_initC, igrid, isim):
        self.n_step = 10000 # note the initial case
        self.max_step = 10000 
        self.n_step_tail = 10  # inst cases need long tail
        
        #self.n_avg = 1000
        
        self.is_inst = 0
        self.n_inst = 1

        self.network_type = network_type
        self.game_type = 'PD' 
        self.N = N
        self.z = z 
        self.beta0 = beta0
        self.beta1 = beta1
        
        if self.n_step >= self.max_step: self.n_step = self.max_step
        
        self.br = br  # b for PD and r for SD
        self.igrid = igrid
        self.isim = isim
        self.is_resume = 1
        
        # payoff
        if self.game_type == 'PD':
            # payoff
            self.R = 1.0  # Reward for mutual cooperation
            self.S = 0.0  # Sucker's payoff
            self.T = self.br  # Temptation to defect
            self.P = 0.0  # Punishment for mutual defection
            
            # D
            self.D = self.T-self.S
        elif self.game_type == 'SD':
            pass
        
        # payoff matrix
        self.payoff_matrix = np.array([[self.R, self.S], [self.T, self.P]])
        
        self.a_initC = a_initC
        
        self.gridEnsembleName = 'network_%s_game_%s_N_%05d_z_%03d_br_%.4f_beta0_%.4f_beta1_%.4f_initC_%.4f_igrid_%04d'%(self.network_type, self.game_type, self.N, self.z, self.br, self.beta0, self.beta1, self.a_initC, self.igrid)  
        self.caseName = self.gridEnsembleName + '_isim_%04d'%(self.isim)  


if __name__ == "__main__":
    
    ngrid = 30
    # ngrid = 100
    
    # nsim = 1
    nsim = 30
    
    N = 200
    
    params_list = []
    for network_type in [
            # 'rg',
            # 'lt',
            # 'rr',
            # 'rd',
            'sf'
            ]:
        
        for z in [4]:
            for br in [
                    
                    # 1.0,
                    # 1.02,
                    # 1.05,
                    # 1.08,
                    # 1.1,
                    # 1.12,
                    # 1.15,
                    # 1.18,
                    # 1.2,
                    
                    1.1, 
                    1.2, 
                    1.3, 
                    1.4, 
                    1.5, 
                    1.6, 
                    1.7, 
                    1.8, 
                    1.9, 
                    ]: 
                
                beta0_beta1_list = [
                                    [0.1, 0.02],
                                    [0.2, 0.1],
                                    [0.4, 0.2],
                                    ]
    
                for beta0_beta1 in beta0_beta1_list:
                    beta0 = beta0_beta1[0]
                    beta1 = beta0_beta1[1]
                    
                    for a_initC in [
                                    # 0.1, 
                                    # 0.3,
                                    0.5,
                                    # 0.7,
                                    ]:
                        for igrid in range(ngrid):
                            for isim in range(nsim):
                                params = params_case(network_type, N, z, br, beta0, beta1, a_initC, igrid, isim)
                                params_list.append(params)
        
    # Parallelize using Pool
    num_processes = 1
    with Pool(num_processes) as pool:
        pool.map(play_case, params_list)

        pool.close()
        pool.join()

    # for params in params_list:
    #     play_case(params)
    
    
 
