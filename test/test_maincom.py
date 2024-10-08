"""This file contains the test cases for the maincom.py file."""

import pytest
from numpy.random import PCG64, Generator

from agenet import run_simulation, simulation

# define test cases
test_cases = [
    (2, 0.9, 300, 100, 10**-2, 700, 1 * (10**-13), 6 * (10**9), 1000, 42),
    (4, 0.5, 500, 50, 50**-2, 700, 1 * (10**-13), 6 * (10**9), 1000, 123),
    (3, 0.7, 400, 75, 25**-2, 800, 2 * (10**-13), 5 * (10**9), 500, 456),
]


@pytest.mark.parametrize(
    "num_nodes, active_prob, n, k, P, d, N0, fr, numevents, seed", test_cases
)
def test_simulation(num_nodes, active_prob, n, k, P, d, N0, fr, numevents, seed):
    """Test the simulation function for various inputs."""
    result = simulation(
        num_nodes, active_prob, n, k, P, d, N0, fr, numevents, seed=seed
    )
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    theoretical, simulated = result
    assert all(isinstance(x, float) for x in result)
    assert theoretical > 0
    assert simulated > 0
    assert (
        abs(theoretical - simulated) < theoretical
    )  # Simulated should be reasonably close to theoretical


def test_simulation_reproducibility():
    """Test that the simulation produces the same results with the same seed."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000)
    seed = 42
    result1 = simulation(*params, seed=seed)
    result2 = simulation(*params, seed=seed)
    assert (
        result1 == result2
    ), "Simulation results are not reproducible with the same seed"


def test_simulation_different_seeds():
    """Test that the simulation produces different results with different seeds."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000)
    result1 = simulation(*params, seed=42)
    result2 = simulation(*params, seed=123)
    assert result1 != result2, "Simulation results are the same with different seeds"


def test_run_simulation():
    """Test the run_simulation function."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, 10)
    result = run_simulation(*params, seed=42)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(x, float) for x in result)
    assert all(x > 0 for x in result)


def test_run_simulation_reproducibility():
    """Test that run_simulation produces the same results with the same seed."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, 10)
    result1 = run_simulation(*params, seed=42)
    result2 = run_simulation(*params, seed=42)
    assert (
        result1 == result2
    ), "Run_simulation results are not reproducible with the same seed"


def test_run_simulation_different_seeds():
    """Test that run_simulation produces different results with different seeds."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, 10)
    result1 = run_simulation(*params, seed=42)
    result2 = run_simulation(*params, seed=123)
    assert (
        result1 != result2
    ), "Run_simulation results are the same with different seeds"


@pytest.mark.parametrize(
    "seed",
    [
        None,
        0,
        1,
        2**32 - 1,
        pytest.param(
            -1, marks=pytest.mark.xfail(reason="Negative seeds are not supported")
        ),
    ],
)
def test_simulation_various_seeds(seed):
    """Test the simulation function with various seed values."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000)

    if seed is not None and seed < 0:
        with pytest.raises(ValueError, match="expected non-negative integer"):
            simulation(*params, seed=seed)
    else:
        result = simulation(*params, seed=seed)
        assert result is not None and all(
            isinstance(x, float) and x > 0 for x in result
        )


def test_simulation_theoretical_consistency():
    """Test that the theoretical result is consistent across multiple runs."""
    params = (2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000)
    theoretical_results = [simulation(*params, seed=i)[0] for i in range(10)]
    assert all(
        x == theoretical_results[0] for x in theoretical_results
    ), "Theoretical results are not consistent"


def test_simulation_edge_cases():
    """Test the simulation function with edge case inputs."""
    # Test with minimum values
    min_result = simulation(1, 0.1, 2, 1, 10**-6, 1, 10**-15, 1 * (10**9), 10, seed=42)
    assert min_result is not None and all(x > 0 for x in min_result)

    # Test with maximum values (adjusted to avoid potential numerical issues)
    max_result = simulation(
        100, 0.99, 1000, 999, 1, 10000, 1e-10, 100 * (10**9), 10000, seed=42
    )
    assert max_result is not None
    
    if max_result[0] == float('inf'):
        assert max_result[1] == float('inf'), "Both theoretical and simulated values should be infinity in extreme cases"
    else:
        assert max_result[0] > 0, "Theoretical value should be positive"
        assert max_result[1] > 0, "Simulated value should be positive"
        assert max_result[0] != float("inf"), "Theoretical value should not be infinity"

def test_simulation_error_handling():
    """Test that the simulation function handles potential errors gracefully."""
    with pytest.raises(ValueError, match="active_prob must be between 0 and 1"):
        simulation(2, 1.1, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)

    with pytest.raises(ValueError, match="n must be greater than 0"):
        simulation(2, 0.9, 0, 50, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)

    with pytest.raises(ValueError, match="k must be greater than 0"):
        simulation(2, 0.9, 100, 0, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)

    with pytest.raises(ValueError, match="k must be less than or equal to n"):
        simulation(2, 0.9, 100, 101, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)

    with pytest.raises(ValueError, match="P must be greater than 0"):
        simulation(2, 0.9, 300, 100, -1, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)

    with pytest.raises(ValueError, match="N0 must be greater than 0"):
        simulation(2, 0.9, 300, 100, 10**-3, 700, -1 * (10**-13), 6 * (10**9), 1000, seed=42)

    with pytest.raises(ValueError, match="fr must be greater than 0"):
        simulation(2, 0.9, 300, 100, 10**-3, 700, 1 * (10**-13), -6 * (10**9), 1000, seed=42)

def test_simulation_input_validation():
    """Test that the simulation function properly validates input parameters."""
    with pytest.raises(ValueError, match="active_prob must be between 0 and 1"):
        simulation(2, -0.1, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="active_prob must be between 0 and 1"):
        simulation(2, 1.1, 300, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="n must be greater than 0"):
        simulation(2, 0.5, 0, 100, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="k must be greater than 0"):
        simulation(2, 0.5, 300, 0, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="k must be less than or equal to n"):
        simulation(2, 0.5, 300, 301, 10**-3, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="P must be greater than 0"):
        simulation(2, 0.5, 300, 100, -1, 700, 1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="N0 must be greater than 0"):
        simulation(2, 0.5, 300, 100, 10**-3, 700, -1 * (10**-13), 6 * (10**9), 1000, seed=42)
    
    with pytest.raises(ValueError, match="fr must be greater than 0"):
        simulation(2, 0.5, 300, 100, 10**-3, 700, 1 * (10**-13), -6 * (10**9), 1000, seed=42)
