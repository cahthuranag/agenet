# Usage
After installing the package, to run the script on your terminal simply run the following command.
To run a simulation with default parameters, the user can use a provided command. The simulation can generate both theoretical and simulated values for various factors such as block lengths, power allocations, packet sizes, activation probabilities, and number of nodes in the network. These values can be presented in the form of tables using following command.
```
ageprint
```

In addition to the tables, the simulation results can also be displayed as plots using the command 
```
ageplot
```

### How to use manincom module
#### Description of the Simulation Parameters

   - `--num_nodes`: Number of nodes in the network (default: 2).
   - `--active_prob`: Probability that a node is active in a given time slot (default: 0.5).
   - `--n`: Number of bits in a block (default: 200).
   - `--k`: Number of bits in a message (default: 150).
   - `--P`: Power of the nodes (default: 0.1).
   - `--numevents`: Number of events (default: 1000).
   - `--numruns`: Number of times to run the simulation (default: 100).

Example command to run the script:

```
python maincom.py --num_nodes 3 --active_prob 0.7 --n 100 --k 50 --P 0.05 --numevents 500 --numruns 50
```

### Plotting AAoI Simulation Results (plot.py)
This script performs simulations to calculate the Average Age of Information (AAoI) for various input parameters and plots the results comparing theoretical and simulated values.
#### Description of the Simulation Parameters
   - `--num_nodes_const`: Constant value for the number of nodes (default: 2).
   - `--active_prob_const`: Constant value for the active probability (default: 0.5).
   - `--n_const`: Constant value for the block length (default: 150).
   - `--k_const`: Constant value for the update size (default: 100).
   - `--P_const`: Constant value for the power (default: 2 * 10**-3).
   - `--numevnts`: Number of events to simulate (default: 1000).
   - `--numruns`: Number of runs for the simulation (default: 100).
   - `--num_nodes_vals`: Variable range for the number of nodes (default: [1, 2, 3, 4, 5]).
   - `--active_prob_vals`: Variable range for the active probability (default: [0.1, 0.15, 0.2, 0.25]).
   - `--n_vals`: Variable range for the block length (default: [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]).
   - `--k_vals`: Variable range for the update size (default: [50, 60, 70, 80, 90, 95, 100]).
   - `--P_vals`: Variable range for the power (default: [2 * 10**-3, 3 * 10**-3, 4 * 10**-3, 5 * 10**-3, 10 * 10**-3]).

Example command to run the script:

```
python aa_simulation_plot.py --num_nodes_const 3 --active_prob_const 0.7 --n_const 200 --k_const 150 --P_const 0.05 --numevnts 500 --numruns 50 --num_nodes_vals  [2, 3, 4, 5] --active_prob_vals [0.3, 0.4, 0.5] --n_vals [100, 200, 300] --k_vals [100, 150, 200] --P_vals [0.01, 0.02, 0.03]
```

## Generating comparison tables

This Python script generates and prints comparison tables for theoretical and simulated data based on specified input values.
#### Description of the Simulation Parameters

- `--num_nodes_const`: Constant value for the number of nodes (default: 2).
- `--active_prob_const`: Constant value for the active probability (default: 0.5).
- `--n_const`: Constant value for the block length (default: 150).
- `--k_const`: Constant value for the update size (default: 100).
- `--P_const`: Constant value for the power (default: 0.002).
- `--numevnts`: The number of events (default: 500).
- `--numruns`: The number of runs (default: 100).
- `--num_nodes_vals`: List of values for the number of nodes (default: [1, 2, 3, 4, 5]).
- `--active_prob_vals`: List of values for the active probability (default: [0.1, 0.15, 0.2, 0.25]).
- `--n_vals`: List of values for the block length (default: [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]).
- `--k_vals`: List of values for the update size (default: [50, 60, 70, 80, 90, 95, 100]).
- `--P_vals`: List of values for the power (default: [0.002, 0.004, 0.006, 0.008]).

### Running the Script
Example code to run the script:
```
python print.py --num_nodes_const 2 --active_prob_const 0.5 --n_const 150 --k_const 100 --P_const 0.002 --numevnts 500 --numruns 100 --num_nodes_vals 1 2 3 4 5 --active_prob_vals 0.1 0.15 0.2 0.25 --n_vals 150 160 170 180 190 200 210 220 230 240 250 --k_vals 50 60 70 
```
