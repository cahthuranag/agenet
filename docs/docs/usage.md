# Usage
After installing the package, to run the script on your terminal simply run the following command.
To run a simulation with default parameters, the user can use a provided command. The simulation can generate both theoretical and simulated values for various factors such as block lengths, power allocations, packet sizes, activation probabilities, and number of nodes in the network. These values can be presented in the form of tables using following command.
```
agenet
```
### How to use manincom module
#### Description of the Simulation Parameters

- `--num_nodes`: Specifies the number of nodes in the network. Default is 2.
- `--active_prob`: Sets the probability that a node is active in a given time slot. Default is 0.5.
- `--n`: Determines the number of bits in a block. Default is 200.
- `--k`: Sets the number of bits in a message. Default is 150.
- `--P`: Defines the power of the nodes. Default is 0.1.
- `--d`: Distance between nodes.
- `--N0`: Noise power.
- `--fr`: Frequency of the signal.
- `--numevents`: Sets the number of events to simulate. Default is 1000.
- `--numruns`: Indicates the number of times the simulation will run. Default is 100.


Example command to run the script:

```
python maincom.py --num_nodes 3 --active_prob 0.7 --n 100 --k 50 --P 0.05 --d 700 --N0 1e-13 --fr 6e9 --numevents 500 --numruns 50

```

## How to use printplot module
### Description
This script is designed for analyzing  average age of information of the network  by generating tables and plots comparing theoretical and simulated values based on various network parameters.

### Command-Line Arguments

#### Constant Parameters
- `--num_nodes_const <int>`: Number of nodes.
- `--active_prob_const <float>`: Active probability of nodes.
- `--n_const <int>`: Block length.
- `--k_const <int>`: Update size.
- `--P_const <float>`: Power level.
- `--d_const <int>`: Distance between nodes.
- `--N0_const <float>`: Noise power.
- `--fr_const <float>`: Frequency of the signal.

#### Variable Parameters
- `--num_nodes_vals <List[int]>`: Varying values for the number of nodes.
- `--active_prob_vals <List[float]>`: Varying values for the active probability.
- `--n_vals <List[int]>`: Varying values for the block length.
- `--k_vals <List[int]>`: Varying values for the update size.
- `--P_vals <List[float]>`: Varying values for the power.

### Simulation Control
- `--numevnts <int>`: Number of events.
- `--numruns <int>`: Number of simulation runs.

### Output Options
- `--quiet`: Suppresses table output.
- `--plots`: Enables plot generation.
- `--plots_folder <str>`: Specifies folder to save plots.

## Usage Example
```
python printplot.py --num_nodes_const 5 --active_prob_const 0.3 --n_const 100 --k_const 50 --P_const 0.002 --d_const 700 --N0_const 1e-13 --fr_const 6e9 --numevnts 500 --numruns 100 --num_nodes_vals 1 2 3 4 5 --active_prob_vals 0.1 0.2 0.3 0.4 --n_vals 100 150 200 --k_vals 50 75 100 --P_vals 0.001 0.002 0.003 --plots
```
