# Agenet Command-Line Interface Usage Guide

After installing the AgeNet package, you can run simulations using the `agenet` command in your terminal. Here's how to use it:

## Basic Usage

To run a simulation with default parameters:

```
agenet
```

Note: This command will run the simulation but won't display results by default.

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

### Relay or Access Point Parameters

These parameters are optional and default to the source node parameters if not specified:

- `--num-bits-2`: Total number of bits in relay or access point
- `--info-bits-2`: Number of information bits in relay or access point
- `--power-2`: Transmission power in Watts in relay or access point
- `--distance-2`: Distance between relay or access point and destination
- `--N0-2`: Noise power in Watts in relay or access point

### Output Options

- `-t`, `--show-table`: Show table with results
- `-o CSV_FILE`, `--save-csv CSV_FILE`: Save results to CSV file
- `-p`, `--show-plot`: Show plot (only valid if exactly one parameter varies)
- `--save-plot IMAGE_FILE`: Save plot to file (only valid if exactly one parameter varies)
- `--debug {0,1,2}`: Level of debugging report if an error occurs (default: 0)
- `--version`: Show program's version number and exit

## Important Note on Plotting

Plotting is only possible when exactly one parameter is varied. If multiple parameters are varied or only default values are used, the plot options will not work.

## Usage Examples

1. Run a simulation with default parameters and show the results table:
   ```
   agenet -t
   ```

2. Run a simulation with custom frequency and number of events, showing the results table:
   ```
   agenet -f 6e9 -e 200 -t
   ```

3. Run a simulation with multiple frequency values and save the results to a CSV file:
   ```
   agenet -f 5e9 6e9 7e9 -t -o results.csv
   ```

4. Run a simulation varying only the distance, show the table and plot, and save the plot to a file:
   ```
   agenet --distance 100 200 300 400 500 -t -p --save-plot distance_vs_aaoi.png
   ```

5. Run a simulation with custom parameters for both source and relay nodes, showing the results table:
   ```
   agenet --num-bits 500 --info-bits 400 --power 1e-2 --distance 600 --num-bits-2 450 --info-bits-2 350 --power-2 8e-3 --distance-2 400 -t
   ```

6. Run a simulation with high verbosity for debugging and show the results table:
   ```
   agenet --debug 2 -t
   ```

7. Run a simulation varying only the power, show the table and plot:
   ```
   agenet --power 1e-3 2e-3 3e-3 4e-3 5e-3 -t -p
   ```

Remember that you can combine multiple parameters and options as needed for your specific simulation requirements. However, if you want to use the plotting feature, ensure that you vary exactly one parameter. Always include the `-t` or `--show-table` option if you want to see the results displayed in the terminal.