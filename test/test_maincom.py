"""This file contains the test cases for the maincom.py file."""
import os
import subprocess

import pytest

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
    ),  # test case 2
]


# define pytest function to test simulation function with multiple test cases
@pytest.mark.parametrize(
    "num_nodes, active_prob, n, k, P, d, N0, fr, numevents", test_cases
)
def test_simulation(num_nodes, active_prob, n, k, P, d, N0, fr, numevents):
    """Test the simulation function for some known inputs and expected outputs."""
    # call the simulation function
    result = simulation(num_nodes, active_prob, n, k, P, d, N0, fr, numevents)
    # assert that the result is not None
    assert result is not None



