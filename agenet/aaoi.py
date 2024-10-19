"""Calculate the average age of information."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import trapezoid


def aaoi_fn(
    receiving_times: NDArray, generation_times: NDArray
) -> tuple[float, NDArray, NDArray]:
    """Calculate the average age of information.

    Args:
      receiving_times: List of receiving times.
      generation_times: List of generation times.

    Returns:
      Average age of information, age, times.
    """
    # Generate times for the time axis
    times: NDArray = np.arange(0, receiving_times[0] + 0.0005, 0.0005)
    num_events = len(receiving_times)

    for i in range(1, num_events):
        dummy = np.arange(receiving_times[i - 1], receiving_times[i] + 0.0001, 0.0001)
        times = np.concatenate((times, dummy))

    # Compute the age for every time instant
    j = 0
    offset = 0
    age = times.copy()

    for i in range(len(times)):
        if times[i] == receiving_times[j]:
            offset = generation_times[j]
            j += 1
        age[i] -= offset

    # Calculate the integral of age over time
    area = trapezoid(age, times)

    # Calculate the average Age of Information
    aaoi = area / times[-1]

    return aaoi, age, times
