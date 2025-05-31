# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 22:00:51 2023

@author: jyzhang
"""

# Import the os module
import os

import sys
sys.path.append('../')
import dir_basic as Dir


# Define the folder path and the file name
folder_path = Dir.step_freqCooperation_dir


workingFile = "existedCaseName.txt"

# Get a list of all files in the folder
fileName_list = os.listdir(folder_path)

# Open the file for writing
with open(workingFile, "w") as f:
    # Write each file name on a new line
    for fileName in fileName_list:
        case_name = fileName.rsplit('.', 1)[0]
        f.write(case_name + "\n")

