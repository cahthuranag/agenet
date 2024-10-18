

# Agenet Usage Guide

## Introduction

Agenet is a Python package designed to estimate the Age of Information (AoI) in cooperative wireless networks. This guide provides comprehensive instructions on how to use the Agenet command-line interface (CLI) to run simulations and analyze results.

## Basic Usage

After installation, you can access the Agenet CLI using the `agenet` command in your terminal. Running the command with no arguments will display the help information:

```
agenet
```

Note: At least one simulation argument is required to run an actual simulation. Simply running `agenet` without any arguments will not start a simulation.

## Simulation Parameters

### General Simulation Parameters

- `-f`, `--frequency`: Signal frequency in Hz (default: 5e9)
- `-e`, `--num-events`: Number of events in a simulation run (default: 100)
- `-r`, `--num-runs`: Number of simulation runs (default: 10)
- `-s`, `--seed`: Seed for random number generator (random by default)

### Node (or Source Node) Parameters

- `--num-bits`: Total number of bits (default: 400)
- `--info-bits`: Number of information bits (default: 350)
- `--power`: Transmission power in Watts (default: 5e-3)
- `--distance`: Distance between nodes in meters (default: 500)
- `--N0`: Noise power in Watts (default: 1e-13)

### Relay-Specific Parameters

These parameters are optional and default to the source node parameters if not specified:

- `--num-bits-2`: Total number of bits in relay
- `--info-bits-2`: Number of information bits in relay
- `--power-2`: Transmission power in Watts in relay
- `--distance-2`: Distance between relay and destination
- `--N0-2`: Noise power in Watts in relay

### Output Options

- `-t`, `--show-table`: Show table with results
- `-o CSV_FILE`, `--save-csv CSV_FILE`: Save results to CSV file
- `-p`, `--show-plot`: Show plot (only valid if exactly one parameter varies)
- `--save-plot IMAGE_FILE`: Save plot to file (only valid if exactly one parameter varies)
- `--debug {0,1,2}`: Level of debugging report if an error occurs (default: 0)
- `--version`: Show program's version number and exit

#### Important Note on Plotting

Plotting is only possible when exactly one parameter is varied. If multiple parameters are varied or only default values are used, the plot options will not work.

## Usage Examples

1. Run a simulation with custom frequency and show the results table:
   ```
   agenet -f 6e9 -t
   ```

2. Run a simulation with multiple frequency values and save the results to a CSV file:
   ```
   agenet -f 5e9 6e9 7e9 -t -o results.csv
   ```

3. Run a simulation varying only the distance, show the table and plot, and save the plot to a file:
   ```
   agenet --distance 100 200 300 400 500 -t -p --save-plot distance_vs_aaoi.png
   ```

4. Run a simulation with custom parameters for both source and relay nodes, showing the results table:
   ```
   agenet --num-bits 500 --info-bits 400 --power 1e-2 --distance 600 --num-bits-2 450 --info-bits-2 350 --power-2 8e-3 --distance-2 400 -t
   ```

5. Run a simulation with high verbosity for debugging and show the results table:
   ```
   agenet --debug 2 -t
   ```

6. Run a simulation varying only the power, show the table and plot:
   ```
   agenet --power 1e-3 2e-3 3e-3 4e-3 5e-3 -t -p
   ```

## Best Practices

1. Always specify at least one simulation parameter to run a simulation.
2. Use the `-t` or `--show-table` option to display results in the terminal.
3. When using plotting features, ensure you vary exactly one parameter.
4. For complex simulations, consider saving results to a CSV file for further analysis.
5. Use the debugging options when encountering issues to get more detailed error information.
