"""This file contains the test cases for the maincom.py file."""

import pytest
from numpy.random import PCG64, Generator

from agenet import simulation

# define test cases
test_cases = [
    (
        2,
        0.9,
        300,
        100,
        10**-3,
        700,
        1 * (10**-13),
        6 * (10**9),
        1000,
        42,  # seed for reproducibility
    ),  # test case 1
    (
        4,
        0.5,
        500,
        50,
        50**-3,
        700,
        1 * (10**-13),
        6 * (10**9),
        1000,
        123,  # different seed for second test case
    ),  # test case 2
]


# define pytest function to test simulation function with multiple test cases
@pytest.mark.parametrize(
    "num_nodes, active_prob, n, k, P, d, N0, fr, numevents, seed", test_cases
)
def test_simulation(num_nodes, active_prob, n, k, P, d, N0, fr, numevents, seed):
    """Test the simulation function for some known inputs and expected outputs."""
    # call the simulation function
    result = simulation(num_nodes, active_prob, n, k, P, d, N0, fr, numevents, seed=seed)
    # assert that the result is not None
    assert result is not None
    # assert that the result is a tuple of two floats
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, float) for x in result)
    # You might want to add more specific assertions here, e.g.:
    # assert result[0] > 0  # theoretical value should be positive
    # assert result[1] > 0  # simulated value should be positive
    # assert abs(result[0] - result[1]) < some_tolerance  # theoretical and simulated values should be close

def test_simulation_reproducibility():
    """Test that the simulation produces the same results with the same seed."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000)
    seed = 42
    result1 = simulation(*params, seed=seed)
    result2 = simulation(*params, seed=seed)
    assert result1 == result2, "Simulation results are not reproducible with the same seed"

def test_simulation_different_seeds():
    """Test that the simulation produces different results with different seeds."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000)
    result1 = simulation(*params, seed=42)
    result2 = simulation(*params, seed=123)
    assert result1 != result2, "Simulation results are the same with different seeds"