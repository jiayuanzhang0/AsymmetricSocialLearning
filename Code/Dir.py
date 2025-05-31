# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 18:04:58 2023

@author: jyzhang
"""

 
import os

import sys
sys.path.append('../../')

root_dir = 'E:/project/selectionStrength/demo/AsymmetricSocialLearning/'


Code_dir = root_dir+'Code/'
sys.path.append(Code_dir)

data_dir = root_dir+'data/'
step_freqCooperation_dir = data_dir+'step_freqCooperation/'
G_ensembleShared_dir = data_dir+'G_ensembleShared/'
G_resume_dir = data_dir+'G_resume/'
G_inst_dir = data_dir+'G_inst/'

post_dir = root_dir+'post/'
step_freqCooperation_figDir = post_dir+'step_freqCooperation/'
freqCooperation_paramMean_dir = post_dir+'freqCooperation_paramMean/'


# capture Dirs
#------------------------------------------------------------------------------
# get all variable names in the current script
DirName_list = [var for var in globals().keys() if '__' not in var]

# get all variable values
DirValue_list = []
for DirName in DirName_list:
    Dir = vars()[DirName]  # find the key value (Dir) according to key name
    if type(Dir) != str: continue
    #print(Dir)
    DirValue_list.append(Dir)
 
# mkdir
for DirValue in DirValue_list:
    if not os.path.exists(DirValue): os.makedirs(DirValue)
#------------------------------------------------------------------------------