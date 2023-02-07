import numpy as np


# import sys
from scipy import special as sp
from maincom import main

# from av_age import validate
import matplotlib.pyplot as plt
import bler
import snr
import pandas as pd
import tabulate as tab
import itertools as intert
import matplotlib.pyplot as plt

# Define the range of values for each parameter
num_nodes = range(2, 3)
active_prob = np.arange(0.1, 0.8, 0.05)


# Combine the parameters into a list
params = [num_nodes, active_prob]
combinations = list(intert.product(*params))
for i, param in enumerate([num_nodes, active_prob]):
    # Create an empty list to store the results of the simulation for the current parameter
    results = []

    # Iterate over each combination of parameters and run the simulation
    for combo in combinations:
        # Unpack the combination into separate variables
        num_nodes, active_prob = combo
        # Run the simulation with the current parameters
        x, y = main(num_nodes, active_prob)
        print(x, y)
        # Append the result of the simulation to the results list
        results.append((combo[i], x, y))

    # Convert the results list to a numpy array
    results = np.array(results)

    # Define the name of the current parameter
    param_names = ["number of nodes", "active probability"]
    param_name = param_names[i]

    # Plot the result
    plt.plot(results[:, 0], results[:, 1], label="x")
    plt.plot(results[:, 0], results[:, 2], label="y")
    plt.xlabel(param_name)
    plt.ylabel("AAoI")
    plt.title("x and y vs {}".format(param_name))
    plt.legend()
    plt.show()
