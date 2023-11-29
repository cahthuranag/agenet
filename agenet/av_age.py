"""Calculate the average age of information."""
import argparse
from typing import List, Tuple

import numpy as np
from scipy.integrate import trapz


# Define the average age of information function
def av_age_fn(
    destination_times: List[float],
    generation_times: List[float],
    lambha: float,
) -> Tuple[float, np.ndarray, np.ndarray]:
    """
    Calculate the AAoI given the parameters.

    Args:
        destination_times (List[float]): A sorted list of destination times.
        generation_times (List[float]): A list of the  generation times.
        lambha (float): The arrival rate of information.

    Returns:
        Tuple[float, np.ndarray, np.ndarray]:  A tuple containing the aaoi, the
        array of ages for each time step, and the corresponding time step array.
    """
    # Define the time step (p) as a constant (lambha)
    p = lambha * 0.01
    # Initialize the times array with the first destination time plus the time
    # step
    times = np.arange(0, destination_times[0] + p, p)
    # Loop through the rest of the destination times
    for i in range(1, len(destination_times)):
        # Generate an array of times between two consecutive destination times
        dummy = np.arange(
            destination_times[i - 1], destination_times[i] + p, p
        )
        # Concatenate the times array with the dummy array
        times = np.concatenate((times, dummy))
    # Initialize a counter (ii) and an offset
    ii = 0
    offset = 0
    # Initialize the age array as the times array
    age = times.copy()
    # Loop through the times array
    for i in range(len(times)):
        # If the current time is equal to a destination time
        if times[i] == destination_times[ii]:
            # Update the offset with the corresponding generation time
            offset = generation_times[ii]
            # Increment the counter
            ii = ii + 1
        # Update the current value in the age array as the difference between
        # the time and the offset
        age[i] = age[i] - offset
    # Calculate the average age as the area under the curve of the age versus
    # time divided by the maximum time
    average_age = trapz(age, times) / np.amax(times)
    # Return the average age, the age array, and the times array
    return average_age, age, times


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate the average age of information."
    )
    parser.add_argument(
        "--lambha",
        type=float,
        default=1,
        help="The arrival rate of information.",
    )
    parser.add_argument(
        "--dest_times",
        nargs="+",
        type=float,
        default=[0.5, 1.5, 2.5, 3.5, 4.5],
        help="Destination times.",
    )
    parser.add_argument(
        "--gen_times",
        nargs="+",
        type=float,
        default=[0.3, 0.8, 1.2, 1.6, 2.0],
        help="Generation times.",
    )
    args = parser.parse_args()

    # Convert destination_times and generation_times to lists
    destination_times = args.dest_times
    generation_times = args.gen_times
    lambha = args.lambha  # Changed variable name to 'lambdha'

    # Call the function with the provided arguments
    average_age, _, _ = av_age_fn(
        destination_times, generation_times, lambha
    )

    # Print the results
    print("Average Age of Information:", average_age)


if __name__ == "__main__":
    _parse_args()
