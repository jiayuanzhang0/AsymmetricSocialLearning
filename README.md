# AsymmetricSocialLearning

This repository contains simulation code and analysis scripts for the paper "Evolution of Cooperation with Asymmetric Social Learning". The model explores how asymmetric payoff sensitivity in strategy update affects evolutionary dynamics in networked populations.

## Installation

1. Create Conda environment:
```bash
conda create --name asymmetric_payoff_sensitivity python=3.9
```
Activate environment:

```bash
conda activate asymmetric_payoff_sensitivity
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Repository Structure
asymmetric/
├── Code/
│   ├── simulation/               # Evolutionary simulation scripts
│   │   └── main.py               # Main simulation driver
│   │
│   └── mean_fc/                  # Analysis and visualization
│       ├── cal_mean_fc.py         # Computes mean frequency of cooperators 
│       └── plot_br_freqCooperation.py  # Generates figure of frequency of cooperators 
│
└── requirements.txt              # Python dependencies

## Running the Simulation and Analysis

1. Perform Evolutionary Simulations
```bash
cd asymmetric/Code/simulation
python main.py
```
Simulates cooperation evolution across parameter space

Output: Time series of frequency of cooperators 

2. Compute Mean Frequency of Cooperators 
```bash
cd asymmetric/Code/mean_fc
python cal_mean_fc.py
```
Calculates mean cooperation frequency over last 1000 time steps of evolution

All simulation replicates

3. Generate Figures
```bash
python plot_br_freqCooperation.py
```
Creates lines of frequency of cooperators vs temptation:

Requirements
Python 3.9

numpy

matplotlib

networkx
