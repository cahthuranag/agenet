"""This file contains the test cases for the maincom.py file."""

import re
from multiprocessing import Value
from threading import Event

import numpy as np
import pytest

from agenet import ev_sim, multi_param_ev_sim, sim

# ############################ #
# Tests for the sim() function #
# ############################ #

# define test cases
test_cases = [
    (6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13), 42),
    (6 * (10**9), 1000, 500, 50, 50**-3, 700, 1 * (10**-13), 123),
    (5 * (10**9), 500, 400, 75, 25**-3, 800, 2 * (10**-13), 456),
]


@pytest.mark.parametrize("fr, num_events, n, k, P, d, N0, seed", test_cases)
def test_sim(n, k, P, d, N0, fr, num_events, seed):
    """Test the sim() function for various inputs."""
    result = sim(fr, num_events, n, k, P, d, N0, seed=seed)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 6
    theoretical = result[0]
    simulated = result[1]
    assert all(isinstance(x, float) for x in result)
    assert theoretical > 0
    assert simulated > 0


def test_sim_reproducibility():
    """Test that the sim() function produces the same results with the same seed."""
    params = (6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13))
    seed = 42
    result1 = sim(*params, seed=seed)
    result2 = sim(*params, seed=seed)
    assert (
        result1 == result2
    ), "Simulation results are not reproducible with the same seed"


def test_sim_different_seeds():
    """Test that the sim() function produces different results with different seeds."""
    params = (6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13))
    result1 = sim(*params, seed=42)
    result2 = sim(*params, seed=123)
    assert result1 != result2, "Simulation results are the same with different seeds"


@pytest.mark.parametrize(
    "seed",
    [
        None,
        0,
        1,
        2**32 - 1,
        -1,
    ],
)
def test_sim_various_seeds(seed):
    """Test the sim() function with various seed values."""
    params = {
        "frequency": 6 * (10**9),
        "num_events": 1000,
        "num_bits": 300,
        "info_bits": 100,
        "power": 10**-3,
        "distance": 700,
        "N0": 1 * (10**-13),
    }

    if seed is not None and seed < 0:
        with pytest.raises(ValueError, match="expected non-negative integer"):
            sim(**params, seed=seed)
    else:
        result = sim(**params, seed=seed)
        assert result is not None
        assert all(isinstance(x, float) and x > 0 for x in result)


def test_sim_theoretical_consistency():
    """Test that the theoretical result is consistent across multiple runs."""
    params = (6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13))
    theoretical_results = [sim(*params, seed=i)[0] for i in range(10)]
    assert all(
        x == theoretical_results[0] for x in theoretical_results
    ), "Theoretical results are not consistent"


def test_sim_edge_cases():
    """Test the sim() function with edge case inputs."""
    # Test with minimum values
    min_result = sim(1 * (10**9), 10, 2, 1, 10**-6, 1, 10**-15, seed=42)
    assert min_result is not None
    assert all(x > 0 for x in min_result)

    # Test with maximum values (adjusted to avoid potential numerical issues)
    max_result = sim(100 * (10**9), 10000, 1000, 999, 1, 10000, 1e-10, seed=42)
    assert max_result is not None

    if max_result[0] == float("inf"):
        assert max_result[1] == float(
            "inf"
        ), "Both theoretical and simulated values should be infinity in extreme cases"
    else:
        assert max_result[0] > 0, "Theoretical value should be positive"
        assert max_result[1] > 0, "Simulated value should be positive"
        assert max_result[0] != float("inf"), "Theoretical value should not be infinity"


@pytest.mark.parametrize(
    "frequency, num_events, num_bits, info_bits, power, distance, N0, num_bits_2, info_bits_2, power_2, distance_2, N0_2, seed, expected_error, match_msg",
    [
        # frequency must be greater than 0 (given negative frequency)
        (
            -6 * (10**9),
            1000,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`frequency` (-6000000000) must be greater than 0",
        ),
        # frequency must be greater than 0 (given zero frequency)
        (
            0,
            1000,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`frequency` (0) must be greater than 0",
        ),
        # num_events must be greater than 0 (given negative number of events)
        (
            6 * (10**9),
            -1000,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`num_events` (-1000) must be greater than 0",
        ),
        # num_events must be greater than 0 (given zero events)
        (
            6 * (10**9),
            0,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`num_events` (0) must be greater than 0",
        ),
        # num_bits must be greater than 0
        (
            6 * (10**9),
            1000,
            0,
            50,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`num_bits` (0) and `num_bits_2` (0) must be greater than 0",
        ),
        # num_bits_2 must be greater than 0
        (
            6 * (10**9),
            1000,
            100,
            50,
            10**-3,
            700,
            1 * (10**-13),
            -100,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`num_bits` (100) and `num_bits_2` (-100) must be greater than 0",
        ),
        # info_bits must be greater than 0
        (
            6 * (10**9),
            1000,
            100,
            0,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`info_bits` (0) and `info_bits_2` (0) must be greater than 0",
        ),
        # info_bits_2 must be greater than 0
        (
            6 * (10**9),
            1000,
            100,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            -100,
            None,
            None,
            None,
            42,
            ValueError,
            "`info_bits` (100) and `info_bits_2` (-100) must be greater than 0",
        ),
        # info_bits must be less than or equal to num_bits
        (
            6 * (10**9),
            1000,
            100,
            101,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`info_bits` (101) must be less than or equal to `num_bits` (100)",
        ),
        # info_bits_2 must be less than or equal to num_bits_2
        (
            6 * (10**9),
            1000,
            100,
            100,
            10**-3,
            700,
            1 * (10**-13),
            100,
            101,
            None,
            None,
            None,
            42,
            ValueError,
            "`info_bits_2` (101) must be less than or equal to `num_bits_2` (100)",
        ),
        # num_bits_2 must be greater than or equal to num_bits
        (
            6 * (10**9),
            1000,
            100,
            100,
            10**-3,
            700,
            1 * (10**-13),
            99,
            99,
            None,
            None,
            None,
            42,
            ValueError,
            "`num_bits_2` (99) must be equal or greater than `num_bits` (100)",
        ),
        # power must be greater than 0
        (
            6 * (10**9),
            1000,
            300,
            100,
            -1,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`power` (-1) and `power_2` (-1) must be greater than 0",
        ),
        # power_2 must be greater than 0
        (
            6 * (10**9),
            1000,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            -(10**-3),
            None,
            None,
            42,
            ValueError,
            "`power` (0.001) and `power_2` (-0.001) must be greater than 0",
        ),
        # distance must be greater than 0
        (
            6 * (10**9),
            1000,
            300,
            100,
            10**-3,
            -700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`distance` (-700) and `distance_2` (-700) must be greater than 0",
        ),
        # distance_2 must be greater than 0
        (
            6 * (10**9),
            1000,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            -10,
            None,
            42,
            ValueError,
            "`distance` (700) and `distance_2` (-10) must be greater than 0",
        ),
        # N0 must be greater than 0
        (
            6 * (10**9),
            1000,
            300,
            100,
            10**-3,
            700,
            -1 * (10**-13),
            None,
            None,
            None,
            None,
            None,
            42,
            ValueError,
            "`N0` (-1e-13) and `N0_2` (-1e-13) must be greater than 0",
        ),
        # N0_2 must be greater than 0
        (
            6 * (10**9),
            1000,
            300,
            100,
            10**-3,
            700,
            1 * (10**-13),
            None,
            None,
            None,
            None,
            -1 * (10**-13),
            42,
            ValueError,
            "`N0` (1e-13) and `N0_2` (-1e-13) must be greater than 0",
        ),
    ],
)
def test_sim_error_handling(
    frequency,
    num_events,
    num_bits,
    info_bits,
    power,
    distance,
    N0,
    num_bits_2,
    info_bits_2,
    power_2,
    distance_2,
    N0_2,
    seed,
    expected_error,
    match_msg,
):
    """Test that the sim() function handles potential errors gracefully."""
    with pytest.raises(expected_error, match=re.escape(match_msg)):
        sim(
            frequency,
            num_events,
            num_bits,
            info_bits,
            power,
            distance,
            N0,
            num_bits_2,
            info_bits_2,
            power_2,
            distance_2,
            N0_2,
            seed=seed,
        )


# ############################### #
# Tests for the ev_sim() function #
# ############################### #


def test_ev_sim():
    """Test the ev_sim function."""
    params = (10, 6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13))
    result = ev_sim(*params, seed=42)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 6
    assert all(isinstance(x, float) for x in result)
    assert all(x > 0 for x in result)


def test_ev_sim_reproducibility():
    """Test that ev_sim() function produces the same results with the same seed."""
    params = (10, 6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13))
    result1 = ev_sim(*params, seed=42)
    result2 = ev_sim(*params, seed=42)
    assert (
        result1 == result2
    ), "Run_simulation results are not reproducible with the same seed"


def test_ev_sim_different_seeds():
    """Test that ev_sim() produces different results with different seeds."""
    params = (10, 6 * (10**9), 1000, 300, 100, 10**-3, 700, 1 * (10**-13))
    result1 = ev_sim(*params, seed=42)
    result2 = ev_sim(*params, seed=123)
    assert (
        result1 != result2
    ), "Run_simulation results are the same with different seeds"


def test_ev_sim_return_inf_aaoi_th():
    """Test that ev_sim() returns infinite ev AAoI when one AAoI is infinite."""
    ev_aaoi_th, ev_aaoi_sim, _, _, _, _ = ev_sim(
        20, 250000000000, 35, 400, 200, 0.005, 500, 1e-13
    )
    assert np.isinf(ev_aaoi_th)
    assert np.isinf(ev_aaoi_sim)


# ########################################### #
# Tests for the multi_param_ev_sim() function #
# ########################################### #


@pytest.mark.parametrize(
    "num_runs, frequency, num_events, num_bits, info_bits, power, distance, N0, num_bits_2, info_bits_2, power_2, distance_2, N0_2, seed, counter, stop_event",
    [
        (
            5,
            [1000],
            [50],
            [100],
            [100],
            [10**-3],
            [700],
            [1 * (10**-13)],
            [None],
            [None],
            [None],
            [None],
            [None],
            42,
            None,
            None,
        ),
        (
            5,
            [1000, 2000],
            [5, 10],
            [100, 300],
            [100, 350],
            [10**-3],
            [700],
            [1 * (10**-13)],
            [None],
            [None],
            [None],
            [None],
            [None],
            42,
            Value("i", 0),
            Event(),
        ),
        (
            2,
            [1500],
            [5],
            [100, 300],
            [100, 350],
            [1e-3],
            [700],
            [1e-13],
            [75, 100, 200, 350],
            [65, 105, 195, 351],
            [1e-3, 2e-3],
            [500, 900],
            [5e-14, 2e-13],
            242,
            Value("i", 0),
            Event(),
        ),
    ],
)
def test_multi_param_ev_sim_ok(
    num_runs,
    frequency,
    num_events,
    num_bits,
    info_bits,
    power,
    distance,
    N0,
    num_bits_2,
    info_bits_2,
    power_2,
    distance_2,
    N0_2,
    seed,
    counter,
    stop_event,
):
    """Test that the multi_param_ev_sim() function works well with valid parameters."""
    df, perrs = multi_param_ev_sim(
        num_runs,
        frequency,
        num_events,
        num_bits,
        info_bits,
        power,
        distance,
        N0,
        num_bits_2,
        info_bits_2,
        power_2,
        distance_2,
        N0_2,
        seed,
        counter,
        stop_event,
    )

    num_results = len(df) + sum(len(v) for v in perrs.values())
    total_param_combos = (
        len(frequency)
        * len(num_events)
        * len(num_bits)
        * len(info_bits)
        * len(power)
        * len(distance)
        * len(N0)
        * len(num_bits_2)
        * len(info_bits_2)
        * len(power_2)
        * len(distance_2)
        * len(N0_2)
    )

    assert num_results == total_param_combos
    assert counter is None or counter.value == num_results
    assert stop_event is None or not stop_event.is_set()


def test_multi_param_ev_sim_stop():
    """Test that multi_param_ev_sim() stops ahead of time given an event signal."""
    frequency = [1250]
    num_events = [7]
    num_bits = [100, 200]
    info_bits = [100]
    power = [1e-3]
    distance = [600]
    n0 = [9e-14]
    same_as_source = [None]

    stop_event = Event()
    stop_event.set()
    df, perrs = multi_param_ev_sim(
        5,
        frequency,
        num_events,
        num_bits,
        info_bits,
        power,
        distance,
        n0,
        same_as_source,
        same_as_source,
        same_as_source,
        same_as_source,
        same_as_source,
        123,
        None,
        stop_event,
    )

    num_results = len(df) + sum(len(v) for v in perrs.values())
    total_param_combos = (
        len(frequency)
        * len(num_events)
        * len(num_bits)
        * len(info_bits)
        * len(power)
        * len(distance)
        * len(n0)
        * len(same_as_source)
        * len(same_as_source)
        * len(same_as_source)
        * len(same_as_source)
        * len(same_as_source)
    )

    assert num_results < total_param_combos
    assert stop_event.is_set()
