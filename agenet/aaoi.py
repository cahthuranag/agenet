"""Calculate the average age of information."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import trapezoid


def aaoi_fn(
    departure_times: NDArray, final_arrival_times: NDArray
) -> tuple[float, NDArray, NDArray]:
    """Calculate the average age of information.

    Args:
        departure_times: List of departure times.
        final_arrival_times: List of final arrival times.

    Returns:
        Average age of information, age, times.
    """
    # Generate times for the time axis
    times: NDArray = np.arange(0, departure_times[0] + 0.0005, 0.0005)
    num_events = len(departure_times)

    for i in range(1, num_events):
        dummy = np.arange(departure_times[i - 1], departure_times[i] + 0.0001, 0.0001)
        times = np.concatenate((times, dummy))

    # Compute the age for every time instant
    j = 0
    offset = 0
    age = times.copy()

    for i in range(len(times)):
        if times[i] == departure_times[j]:
            offset = final_arrival_times[j]
            j += 1
        age[i] -= offset

    # Calculate the integral of age over time
    area = trapezoid(age, times)

    # Calculate the average Age of Information
    aaoi = area / times[-1]

    return aaoi, age, times
