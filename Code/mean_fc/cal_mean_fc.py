# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:23:27 2023

@author: jyzhang
"""

import numpy as np
import os

import sys
sys.path.append('../')
import Dir

load_dir = Dir.step_freqCooperation_dir
fileName_list = os.listdir(load_dir)
fileName_list.sort()
  
from collections import defaultdict

def group_string(strings):
    grouped_strings = defaultdict(list)
    
    for s in strings:
        key = s.split("_igrid")[0]
        grouped_strings[key].append(s)
    
    grouped_strings = dict(grouped_strings)  # Convert defaultdict to regular dict for better display
    return grouped_strings

grouped_fileName = group_string(fileName_list)


for key, fileNames in grouped_fileName.items():
    
    series = {}
    series['seriesName'] = key
    parts = key.split('_')
    for i in range(0, len(parts), 2):
        paramName = parts[i]
        paramValue = parts[i+1]
        try:
            if '.' in paramValue:
                paramValue = float(paramValue)
            else:
                paramValue = int(paramValue)
        except ValueError:
            pass
        series[paramName] = paramValue
    
    if series['network'] not in [
                        # 'rg'
                        # 'lt'
                        # 'rr',
                        # 'rd'
                        'sf'
                        ]: continue
    
    # if series['N'] not in [
    #                     # 100,
    #                     200,
    #                     # 512,
    #                     # 10000
    #                     ]: continue

    # if series['initC'] not in [
    #                     # 0.1,
    #                     # 0.3,
    #                     0.5,
    #                     # 0.7,
    #                     ]: continue
    
    freqCooperation_meanLast_list = []
    for fileName in fileNames:

        step_freqCooperation = np.loadtxt(load_dir+fileName) 
            
        # the last part of the time series 
        n_avg = 10
        if len(step_freqCooperation) == 10001:
            # print('not converge')
            n_avg = 1000
        freqCooperation_meanLast = np.mean(step_freqCooperation[-n_avg:,1])
        freqCooperation_meanLast_list.append(freqCooperation_meanLast)
        
    freqCooperation_meanLast_list = np.array(freqCooperation_meanLast_list)
    freqCooperation_meanLast_paramMean = np.mean(freqCooperation_meanLast_list)
    freqCooperation_meanLast_paramMean = np.array([freqCooperation_meanLast_paramMean])
    
    print(key)
    print(freqCooperation_meanLast_paramMean)
    print()
        
    np.savetxt(Dir.freqCooperation_paramMean_dir + key +'.txt', 
               freqCooperation_meanLast_paramMean, 
               fmt='%f')
    

