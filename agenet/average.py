import numpy as np
from scipy.integrate import trapz
import matplotlib.pyplot as plt

# Define the average age of information function
def average_age_of_information_fn(destination_times, generation_times, lambha):
    # Define the time step (p) as a constant (lambha)
    p = lambha * 0.1
    # Initialize the times array with the first destination time plus the time step
    times = np.arange(0, destination_times[0] + p, p)
    # Loop through the rest of the destination times
    for i in range(1, len(destination_times)):
        # Generate an array of times between two consecutive destination times
        dummy = np.arange(destination_times[i - 1], destination_times[i] + p, p)
        # Concatenate the times array with the dummy array
        times = np.concatenate((times, dummy))
    # Initialize a counter (ii) and an offset
    ii = 1
    offset = 0
    # Initialize the age array as the times array
    age = times
    # Loop through the times array
    for i in range(len(times)):
        # If the current time is equal to a destination time
        if times[i] == destination_times[ii]:
            # Update the offset with the corresponding generation time
            offset = generation_times[ii]
            # Increment the counter
            ii = ii + 1
        # Update the current value in the age array as the difference between the time and the offset
        age[i] = age[i] - offset
    # Calculate the average age as the area under the curve of the age versus time divided by the maximum time
    average_age = trapz(age, times) / np.amax(times)
    # Return the average age, the age array, and the times array
    return average_age, age, times


# Define a function to plot and print the example average age of information
def print_average_age_example():
    # Calculate the average age of information for the example
    average_age, age, times = average_age_of_information_fn(
        list(range(1, 10001)), list(range(0, 10000)), 0.1
    )
    # Plot the age versus time
    plt.plot(age, times)
    plt.xlabel("Time")
    plt.ylabel("Age")
    plt.show()
    # Print the average age of information
    print(
        "Average age of information when the destination times are [2,3,4,5], [1,2,3,4]:",
        average_age,
    )


# Call the print_average_age_example function
