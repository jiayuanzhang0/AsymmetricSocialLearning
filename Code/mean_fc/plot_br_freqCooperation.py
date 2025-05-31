# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:23:27 2023

@author: jyzhang
"""

import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.serif'] = 'Times New Roman'
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['xtick.direction']='in'  
matplotlib.rcParams['ytick.direction']='in'  

import os
import sys
sys.path.append('../')
import Dir


load_dir = Dir.freqCooperation_paramMean_dir
fileName_list = os.listdir(load_dir)
fileName_list.sort()

case_list = []
for fileName in fileName_list:
    caseName = fileName.rsplit('.', 1)[0]
    print(caseName)
    
    case = {}
    case['caseName'] = caseName
    case['fileName'] = fileName
    parts = caseName.split('_')
    for i in range(0, len(parts), 2):
        key = parts[i]
        value = parts[i+1]
        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass
        case[key] = value
    
    if case['network'] not in [
                        # 'rg'
                        # 'lt'
                        # 'rr',
                        # 'rd'
                        'sf'
                        ]: continue
    
    # if case['N'] not in [
    #                     # 100,
    #                     200,
    #                     # 512,
    #                     # 10000           
    #                     ]: continue
    
    # if case['initC'] not in [
    #                     # 0.1
    #                     # 0.3,
    #                     0.5,
    #                     # 0.7
    #                     ]: continue
    
    # if case['br'] not in [
    #                     1.1, 
    #                     1.2, 
    #                     1.3, 
    #                     1.4, 
    #                     1.5, 
    #                     1.6, 
    #                     1.7, 
    #                     1.8, 
    #                     1.9, 
    #                     ]: continue

    # beta0_beta1_list = [
    #                                 [0.1, 0.02],
    #                                 [0.2, 0.1],
    #                                 [0.4, 0.2],      
    #     ]
    # if [case['beta0'], case['beta1']] not in beta0_beta1_list: continue  
    
    case_list.append(case)
    
    
# load data of all cases and append data to case
for case in case_list:
    fileName = case['fileName']
    freqCooperation_paramMean = np.loadtxt(load_dir+fileName) 
    case['freqCooperation_paramMean'] = freqCooperation_paramMean
    

# Grouping the cases
caseGroup_dict = {}
for case in case_list:
    groupKey_str1 = 'beta0'
    groupKey_str2 = 'beta1'
    groupKey = tuple([case[groupKey_str1], case[groupKey_str2]])
 
    if groupKey not in caseGroup_dict: caseGroup_dict[groupKey] = []
    caseGroup_dict[groupKey].append(case)

caseGroup_dict = dict(sorted(caseGroup_dict.items()))
#caseGroup_dict.keys()

# plot
#------------------------------------------------------------------------------
fontsize_set = 25

fig = plt.figure(1, figsize=(8,8))  
ax20 = fig.add_subplot(1, 1 ,1)

for groupKey in caseGroup_dict:
    print(groupKey)
    group = caseGroup_dict[groupKey]
    
    x_groupList = []    
    y_groupList = []    
    for case in group:
        x_str = 'br'
        x_groupList.append(case[x_str])
        y_groupList.append(case['freqCooperation_paramMean'])
    
    x_groupList = np.array(x_groupList)
    y_groupList = np.array(y_groupList)
    
    # save figData
    #-------------
    figData = np.zeros((len(x_groupList), 2))
    figData[:,0] = x_groupList
    figData[:,1] = y_groupList
    figData_Dir = './figData/'
    if not os.path.exists(figData_Dir): os.makedirs(figData_Dir)
    figData_Path = figData_Dir + 'network_%s_N_%05d_%s_%.4f_%s_%.4f_initC_%.4f.txt'%(case['network'], case['N'], groupKey_str1, groupKey[0], groupKey_str2, groupKey[1], case['initC'])
    np.savetxt(figData_Path, figData)
    #-------------
 
    ax20.set_xlim(1.0, 2.0)
    ax20.set_ylim(-0.05, 1.05)
    
    if groupKey[0] == groupKey[1]:
        linestyle_set='--'
    else:
        linestyle_set='-'
    
    ax20.plot(x_groupList, y_groupList, 
              linestyle=linestyle_set,
              marker='o',
              markerfacecolor='None',
              label = '$%s=%.4f, %s=%.4f$'%(groupKey_str1, groupKey[0], groupKey_str2, groupKey[1]),
              )
    
    ax20.set_xlabel('$b$', 
                    fontsize=fontsize_set, 
                    )    
    ax20.set_ylabel('$frequency \ of \ cooperators$', 
                    fontsize=fontsize_set, 
                    )     
    ax20.tick_params(labelsize=fontsize_set)    

legend = ax20.legend(
                    fontsize=fontsize_set*0.6, 
                    fancybox=False, framealpha=1, edgecolor='black',
                    )

savePath = './fc.png'
print(savePath)

plt.savefig(savePath, 
            # dpi=600, 
            # bbox_inches='tight'
            ) 
 
# plt.close(fig)    
#------------------------------------------------------------------------------
    
    



