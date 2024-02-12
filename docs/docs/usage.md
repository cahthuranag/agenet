# Usage
After installing the package, to run the script on your terminal simply run the following command.
To run a simulation with default parameters, the user can use a provided command. The simulation can generate both theoretical and simulated values for various factors such as block lengths, power allocations, packet sizes, activation probabilities, and number of nodes in the network. These values can be presented in the form of tables using following command.
```
agenet
```



## How to use agenet module
### Description of the Simulation Parameters

- `--num_nodes_const <int>`: Specifies the number of nodes in the network. Default is 2.
- `--active_prob_const <float>`: Sets the probability that a node is active in a given time slot. Default is 0.5.
- `--n_const <int>`: Determines the number of bits in a block. Default is 150.
- `--k_const <int>`: Sets the number of bits in a message. Default is 100.
- `--P_const <float>`: Defines the power of the nodes. Default is 0.002.
- `--d_const <int>`: Distance between nodes. Default is 700.
- `--N0_const <float>`: Noise power. Default is 1e-13.
- `--fr_const <float>`: Frequency of the signal. Default is 6e9.
- `--numevnts <int>`: Sets the number of events to simulate. Default is 500.
- `--numruns <int>`: Indicates the number of times the simulation will run. Default is 100.

### Variable Parameters
- `--num_nodes_vals <List[int]>`: Varying values for the number of nodes.
- `--active_prob_vals <List[float]>`: Varying values for the active probability.
- `--n_vals <List[int]>`: Varying values for the block length.
- `--k_vals <List[int]>`: Varying values for the update size.
- `--P_vals <List[float]>`: Varying values for the power.

### Simulation Control
- `--quiet`: Suppresses table output.
- `--plots`: Enables plot generation.
- `--plots_folder <str>`: Specifies folder to save plots.
- `--blockerror`: Show theoretical block error.
- `--snr`: Show SNR.
- `--csv_location <str>`: Location to save CSV file.

## Usage Examples

Basic simulation with default parameters:
``` 
agenet 
```
Run simulation with specific parameters and generate plots:
```
agenet --num_nodes_const 3 --active_prob_const 0.7 --n_const 100 --k_const 50 --P_const 0.05 --d_const 700 --N0_const 1e-13 --fr_const 6e9 --plots
```
Calculate theoretical block error rate for a given SNR:
   
``` 
agenet --num_nodes_const 5 --active_prob_const 0.3 --n_const 100 --k_const 50 --P_const 0.002 --d_const 700 --N0_const 1e-13 --fr_const 6e9 --blockerror
```
   
Calculate SNR for a given configuration:
  
``` 
agenet --num_nodes_const 5 --active_prob_const 0.3 --n_const 100 --k_const 50 --P_const 0.002 --d_const 700 --N0_const 1e-13 --fr_const 6e9 --sn
```
Generate plots for various network configurations:
```
agenet --num_nodes_const 5 --active_prob_const 0.3 --n_const 100 --k_const 50 --P_const 0.002 --d_const 700 --N0_const 1e-13 --fr_const 6e9 --plots --plots_folder ./output_plots
```
Run multiple simulations with different parameters and save results to CSV:
   
```
agenet --num_nodes_vals 3 4 5 --active_prob_vals 0.1 0.2 0.3 --n_vals 150 200 250 --k_vals 50 100 --P_vals 0.001 0.002 --csv_location ./results.csv
```