# AsymmetricSocialLearning

This repository contains simulation code and analysis scripts for the paper "Evolution of Cooperation with Asymmetric Social Learning". The model explores how asymmetric payoff sensitivity in strategy update affects evolutionary dynamics in networked populations.

## Installation

```bash
conda create --name asymmetric_payoff_sensitivity python=3.9
conda activate asymmetric_payoff_sensitivity
pip install -r requirements.txt
```

## Running the simulation and analysis

1. Perform evolutionary simulations
```bash
cd asymmetric/Code/simulation
python main.py
```
This simulates the evolution process across the parameter space.

Output: time series of frequency of cooperators.

2. Compute mean equilibrium frequency of cooperators 
```bash
cd asymmetric/Code/mean_fc
python cal_mean_fc.py
```
This calculates mean cooperation frequency over last 1000 time steps of evolution for each parameter set.

3. Visualize the results
```bash
python plot_br_freqCooperation.py
```
This creates lines of frequency of cooperators vs temptation.
