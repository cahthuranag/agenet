"""Module containing core communication system simulation."""

from __future__ import annotations

import itertools
from collections import namedtuple
from collections.abc import MutableSequence, Sequence
from multiprocessing.sharedctypes import Synchronized
from threading import Event
from typing import NamedTuple, cast

import numpy as np
import pandas as pd
from numpy.random import PCG64DXSM, Generator, Philox

from .aaoi import aaoi_fn
from .blkerr import block_error, block_error_th
from .snratio import snr, snr_avg


class _SimParams(NamedTuple):
    """Read-only container for parsed simulation parameters."""

    frequency: float
    """Signal frequency in Hertz."""

    num_events: int
    """Number of events to simulate."""

    num_bits_1: int
    """Number of bits in a block for the source node."""

    info_bits_1: int
    """Number of bits in a message for the source node."""

    power_1: float
    """Power in Watts (source node)."""

    distance_1: float
    """Distance between source node and relay."""

    N0_1: float
    """Noise power for the source node."""

    snr1_avg: float
    """Average SNR for the source node."""

    blkerr1_th: float
    """Theoretical block error for the source node."""

    num_bits_2: int
    """Number of bits in a block for the relay or access point."""

    info_bits_2: int
    """Number of bits in a message for the relay or access point."""

    power_2: float
    """Power in Watts (relay or access point)."""

    distance_2: float
    """Distance between source node and destination."""

    N0_2: float
    """Noise power for the relay or access point."""

    snr2_avg: float
    """Average SNR for the relay or access point."""

    blkerr2_th: float
    """Theoretical block error for the relay or access point."""

    rng: Generator
    """Pseudo-random number generator to use for the simulation."""


class _SimParamError(ValueError):
    """Thrown when a simulation parameter or parameter combination is invalid."""

    pass


def _param_validate(
    frequency: float,
    num_events: int,
    num_bits: int,
    info_bits: int,
    power: float,
    distance: float,
    N0: float,
    num_bits_2: int | None = None,
    info_bits_2: int | None = None,
    power_2: float | None = None,
    distance_2: float | None = None,
    N0_2: float | None = None,
    seed: int | np.signedinteger | None = None,
) -> _SimParams:
    """Check given simulation parameters and return object with final parameters."""
    # Distance between the relay and destination
    if distance_2 is None:
        distance_2 = distance

    # Power of the relay or access point
    if power_2 is None:
        power_2 = power

    # Number of bits in the block for the relay or access point
    if num_bits_2 is None:
        num_bits_2 = num_bits

    # Number of bits in the message for the relay or access point
    if info_bits_2 is None:
        info_bits_2 = info_bits

    # Noise power for the relay or access point
    if N0_2 is None:
        N0_2 = N0

    # Input validation
    if frequency <= 0:
        raise _SimParamError(f"`frequency` ({frequency}) must be greater than 0")
    if num_events <= 0:
        raise _SimParamError(f"`num_events` ({num_events}) must be greater than 0")
    if num_bits <= 0 or num_bits_2 <= 0:
        raise _SimParamError(
            f"`num_bits` ({num_bits}) and `num_bits_2` ({num_bits_2}) must be greater than 0"
        )
    if info_bits <= 0 or info_bits_2 <= 0:
        raise _SimParamError(
            f"`info_bits` ({info_bits}) and `info_bits_2` ({info_bits_2}) must be greater than 0"
        )
    if info_bits > num_bits:
        raise _SimParamError(
            f"`info_bits` ({info_bits}) must be less than or equal to `num_bits` ({num_bits})"
        )
    if info_bits_2 > num_bits_2:
        raise _SimParamError(
            f"`info_bits_2` ({info_bits_2}) must be less than or equal to `num_bits_2` ({num_bits_2})"
        )
    if power <= 0 or power_2 <= 0:
        raise _SimParamError(
            f"`power` ({power}) and `power_2` ({power_2}) must be greater than 0"
        )
    if distance <= 0 or distance_2 <= 0:
        raise _SimParamError(
            f"`distance` ({distance}) and `distance_2` ({distance_2}) must be greater than 0"
        )
    if N0 <= 0 or N0_2 <= 0:
        raise _SimParamError(f"`N0` ({N0}) and `N0_2` ({N0_2}) must be greater than 0")

    # Check that num_bits_2 >= num_bits_1
    if num_bits_2 < num_bits:
        raise _SimParamError(
            f"`num_bits_2` ({num_bits_2}) must be equal or greater than `num_bits` ({num_bits})"
        )

    # Initialize PCG64DXSM generator
    rng = Generator(PCG64DXSM(seed))

    # Determine the average SNR for the two nodes
    snr1_avg = snr_avg(N0, distance, power, frequency)
    snr2_avg = snr_avg(N0_2, distance_2, power_2, frequency)

    # Block error rate at the relay node

    er1_th = block_error_th(snr1_avg, num_bits, info_bits)

    # Block error rate at the destination node
    er2_th = block_error_th(snr2_avg, num_bits_2, info_bits_2)

    # Return validate parameter object
    return _SimParams(
        frequency=frequency,
        num_events=num_events,
        num_bits_1=num_bits,
        info_bits_1=info_bits,
        power_1=power,
        distance_1=distance,
        N0_1=N0,
        snr1_avg=snr1_avg,
        blkerr1_th=er1_th,
        num_bits_2=num_bits_2,
        info_bits_2=info_bits_2,
        power_2=power_2,
        distance_2=distance_2,
        N0_2=N0_2,
        snr2_avg=snr2_avg,
        blkerr2_th=er2_th,
        rng=rng,
    )


def _sim(
    frequency: float,
    num_events: int,
    num_bits_1: int,
    info_bits_1: int,
    power_1: float,
    distance_1: float,
    N0_1: float,
    blkerr1_th: float,
    num_bits_2: int,
    info_bits_2: int,
    power_2: float,
    distance_2: float,
    N0_2: float,
    blkerr2_th: float,
    rng: Generator,
) -> tuple[float, float]:
    """Low-level function for simulating a communication system and obtaining the AAoI.

    This function assumes that all parameters are valid correct, and requires a
    previously instantiated pseudo-random number generator. It's used internally
    by `sim()` and `ev_sim()`.

    Args:
      frequency: Signal frequency in Hertz.
      num_events: Number of events to simulate.
      num_bits_1: Number of bits in a block for the source node.
      info_bits_1: Number of bits in a message for the source node.
      power_1: Power in Watts (source node).
      distance_1: Distance between source node and relay.
      N0_1: Noise power for the source node.
      blkerr1_th: Theoretical block error for the source node.
      num_bits_2: Number of bits in a block for the relay or access point.
      info_bits_2: Number of bits in a message for the relay or access point.
      power_2: Power in Watts (relay or access point).
      distance_2: Distance between source node and destination.
      N0_2: Noise power for the relay or access point.
      blkerr2_th: Theoretical block error for the relay or access point.
      rng: Pseudo-random number generator to use for the simulation.

    Returns:
      A tuple containing the theoretical AAoI and the simulation AAoI.
    """
    # symbol time
    symbol_time = 60e-6

    # Transmission period
    transmission_period = (num_bits_1 + num_bits_2) * symbol_time

    # Inter-arrival times
    inter_arrival_times = transmission_period * (np.ones(num_events))

    # Arrival timestamps
    arrival_timestamps = np.cumsum(inter_arrival_times)

    # Inter-service times
    inter_service_times = transmission_period * np.ones((num_events))

    # Generating departure timestamps for node 1
    server_timestamps_1 = np.zeros(num_events)
    departure_timestamps_s = np.zeros(num_events)

    er_p_th = blkerr1_th + (blkerr2_th * (1 - blkerr1_th))

    for i in range(0, num_events):

        # SNR for the source nodes at the relay or access point
        snr1 = snr(N0_1, distance_1, power_1, frequency, seed=rng)
        snr2 = snr(N0_2, distance_2, power_2, frequency, seed=rng)

        # block error rate for the source nodes at the relay or access point
        er1 = block_error(snr1, num_bits_1, info_bits_1)

        # block error rate for the relay or access point at the destination
        er2 = block_error(snr2, num_bits_2, info_bits_2)

        er_p = er1 + (er2 * (1 - er1))
        er_indi = int(rng.random() > er_p)

        if er_indi == 0:
            # If the packet is not successfully decoded at the destination,
            # departure timestamp is set to nan
            departure_timestamps_s[i] = np.nan
            server_timestamps_1[i] = np.nan
        else:
            departure_timestamps_s[i] = arrival_timestamps[i] + inter_service_times[i]
            server_timestamps_1[i] = arrival_timestamps[i]

    dep = [x for x in departure_timestamps_s if not np.isnan(x)]
    sermat = [x for x in server_timestamps_1 if not np.isnan(x)]

    # Choose a small threshold
    if abs(1 - er_p_th) < 1e-20:
        return float("inf"), float("inf")

    aaoi_th = (transmission_period) * (0.5 + (1 / (1 - er_p_th)))

    # if dep and sermat are empty, return infinity
    if not dep or not sermat:
        return float("inf"), float("inf")
    if np.isnan(departure_timestamps_s[-1]):
        last_dep = arrival_timestamps[-1] + inter_service_times[-1]
        depature_mat = dep + [last_dep]
        arrival_mat = [0] + sermat[1:] + [arrival_timestamps[-1]]
    else:
        depature_mat = dep
        arrival_mat = [0] + sermat[1:]

    aaoi_sim, _, _ = aaoi_fn(depature_mat, arrival_mat)

    return aaoi_th, aaoi_sim


def sim(
    frequency: float,
    num_events: int,
    num_bits: int,
    info_bits: int,
    power: float,
    distance: float,
    N0: float,
    num_bits_2: int | None = None,
    info_bits_2: int | None = None,
    power_2: float | None = None,
    distance_2: float | None = None,
    N0_2: float | None = None,
    seed: int | np.signedinteger | None = None,
) -> tuple[float, float, float, float, float, float]:
    """Simulates a communication system and calculates the AAoI.

    Args:
      frequency: Signal frequency in Hertz.
      num_events: Number of events to simulate.
      num_bits: Number of bits in a block.
      info_bits: Number of bits in a message.
      power: Transmission power in Watts.
      distance: Distance between nodes.
      N0: Noise power in Watts.
      num_bits_2: Number of bits in a block at relay or access point.
      info_bits_2: Number of bits in a message at relay or access point.
      power_2: Transmission power in Watts at relay or access point.
      distance_2: Distance between relay or access point and the destination.
      N0_2: Noise power in Watts at relay or access point.
      seed: Seed for the random number generator (optional).

    Returns:
       A tuple containing: theoretical AAoI, simulation AAoI, theoretical SNR at
         source node, theoretical SNR at relay or access point, theoretical block
         error at source node, theoretical SNR at relay or access point.
    """
    # Parse params and get an object of validated simulation parameters
    params = _param_validate(
        frequency=frequency,
        num_events=num_events,
        num_bits=num_bits,
        info_bits=info_bits,
        power=power,
        distance=distance,
        N0=N0,
        num_bits_2=num_bits_2,
        info_bits_2=info_bits_2,
        power_2=power_2,
        distance_2=distance_2,
        N0_2=N0_2,
        seed=seed,
    )

    # Call the low-level function to actually perform the simulation
    return (
        *_sim(
            frequency=params.frequency,
            num_events=params.num_events,
            num_bits_1=params.num_bits_1,
            info_bits_1=params.info_bits_1,
            power_1=params.power_1,
            distance_1=params.distance_1,
            N0_1=params.N0_1,
            blkerr1_th=params.blkerr1_th,
            num_bits_2=params.num_bits_2,
            info_bits_2=params.info_bits_2,
            power_2=params.power_2,
            distance_2=params.distance_2,
            N0_2=params.N0_2,
            blkerr2_th=params.blkerr2_th,
            rng=params.rng,
        ),
        params.snr1_avg,
        params.snr2_avg,
        params.blkerr1_th,
        params.blkerr2_th,
    )


def ev_sim(
    num_runs: int,
    frequency: float,
    num_events: int,
    num_bits: int,
    info_bits: int,
    power: float,
    distance: float,
    N0: float,
    num_bits_2: int | None = None,
    info_bits_2: int | None = None,
    power_2: float | None = None,
    distance_2: float | None = None,
    N0_2: float | None = None,
    seed: int | np.signedinteger | None = None,
) -> tuple[float, float, float, float, float, float]:
    """Run the simulation `num_runs` times and return the AAoI expected value.

    Args:
      num_runs: Number of times to run the simulation.
      frequency: Signal frequency in Hertz.
      num_events: Number of events to simulate.
      num_bits: Number of bits in a block.
      info_bits: Number of bits in a message.
      power: Transmission power in Watts.
      distance: Distance between nodes.
      N0: Noise power in Watts.
      num_bits_2: Number of bits in a block at relay or access point.
      info_bits_2: Number of bits in a message at relay or access point.
      power_2: Transmission power in Watts at relay or access point.
      distance_2: Distance between relay or access point and the destination.
      N0_2: Noise power in Watts at relay or access point.
      seed: Seed for the random number generator (optional).

    Returns:
      A tuple containing the expected value for the theoretical AAoI and the
        simulation AAoI.
    """
    # Parse params and get an object of validated simulation parameters
    params = _param_validate(
        frequency=frequency,
        num_events=num_events,
        num_bits=num_bits,
        info_bits=info_bits,
        power=power,
        distance=distance,
        N0=N0,
        num_bits_2=num_bits_2,
        info_bits_2=info_bits_2,
        power_2=power_2,
        distance_2=distance_2,
        N0_2=N0_2,
        seed=seed,
    )

    ev_aaoi_th_run = 0.0
    ev_aaoi_sim_run = 0.0

    for _ in range(num_runs):

        # Run the simulation
        av_aaoi_th_i, av_aaoi_sim_i = _sim(
            frequency=params.frequency,
            num_events=params.num_events,
            num_bits_1=params.num_bits_1,
            info_bits_1=params.info_bits_1,
            power_1=params.power_1,
            distance_1=params.distance_1,
            N0_1=params.N0_1,
            blkerr1_th=params.blkerr1_th,
            num_bits_2=params.num_bits_2,
            info_bits_2=params.info_bits_2,
            power_2=params.power_2,
            distance_2=params.distance_2,
            N0_2=params.N0_2,
            blkerr2_th=params.blkerr2_th,
            rng=params.rng,
        )

        # Return infinity for both if theoretical is infinity
        if np.isinf(av_aaoi_th_i):
            return (
                float("inf"),
                float("inf"),
                params.snr1_avg,
                params.snr2_avg,
                params.blkerr1_th,
                params.blkerr2_th,
            )

        # Sum the AAoI's
        ev_aaoi_th_run += av_aaoi_th_i
        ev_aaoi_sim_run += av_aaoi_sim_i

    # Divide the AAoI's by the number of runs to get the expected value (mean)
    ev_aaoi_th_run /= num_runs
    ev_aaoi_sim_run /= num_runs

    # Return results
    return (
        ev_aaoi_th_run,
        ev_aaoi_sim_run,
        params.snr1_avg,
        params.snr2_avg,
        params.blkerr1_th,
        params.blkerr2_th,
    )


def multi_param_ev_sim(
    num_runs: int,
    frequency: Sequence[float],
    num_events: Sequence[int],
    num_bits: Sequence[int],
    info_bits: Sequence[int],
    power: Sequence[float],
    distance: Sequence[float],
    N0: Sequence[float],
    num_bits_2: Sequence[int | None] = [None],
    info_bits_2: Sequence[int | None] = [None],
    power_2: Sequence[float | None] = [None],
    distance_2: Sequence[float | None] = [None],
    N0_2: Sequence[float | None] = [None],
    seed: int | np.signedinteger | None = None,
    counter: Synchronized[int] | None = None,
    stop_event: Event | None = None,
) -> tuple[pd.DataFrame, dict[str, Sequence[NamedTuple]]]:
    """Run the simulation for multiple parameters and return the results.

    Args:
      num_runs: Number of times to run the simulation.
      frequency: List of frequencies.
      num_events: List of number of events.
      num_bits: List of number of bits in a block.
      info_bits: List of number of bits in a message.
      power: List of powers.
      distance: List of distances between nodes.
      N0: List of noise powers.
      num_bits_2: List of number of bits in a block for relay or access point
        (optional, if different than source).
      info_bits_2: List of number of bits in a message for relay or access point
        (optional, if different than source).
      power_2: List of powers for relay or access point
        (optional, if different than source).
      distance_2: List of distances between nodes for relay or access point
        (optional, if different than source).
      N0_2: List of noise powers for relay or access point (optional, if
        different than source).
      seed: Seed for the random number generator (optional).
      counter: An optional `multiprocessing.Value` which will be incremented
        after each inner loop pass. Only relevant if this function is executed
        in a separate thread.
      stop_event: The simulation will stop if this optional event is set
        externally. Only relevant if this function is executed in a separate
        thread.

    Returns:
      A tuple containing a DataFrame with the results of the simulation and a
        log highlighting invalid parameters or parameter combinations.
    """
    rng = Generator(Philox(seed))

    results = []

    param_error_log: dict[str, Sequence[NamedTuple]] = {}

    # Define the named tuple
    ParamCombo = namedtuple(
        "ParamCombo",
        [
            "frequency",
            "num_events",
            "num_bits",
            "info_bits",
            "power",
            "distance",
            "N0",
            "num_bits_2",
            "info_bits_2",
            "power_2",
            "distance_2",
            "N0_2",
        ],
    )

    # Get all combinations and create a parameter combo for each combination
    combos = [
        ParamCombo(f, e, n1, k1, p1, d1, n01, n2, k2, p2, d2, n02)
        for f, e, n1, k1, p1, d1, n01, n2, k2, p2, d2, n02 in itertools.product(
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
        )
    ]

    # Obtain PRNG seeds for each combo
    seeds = rng.integers(np.iinfo(np.int64).max, size=len(combos), dtype=np.int64)

    # Perform `num_runs` simulations for each parameter combo and get the
    # expected value of the AAoI for each combination
    for combo, seed in zip(combos, seeds):

        try:
            (
                aaoi_th,
                aaoi_sim,
                snr1_avg,
                snr2_avg,
                blkerr1_th,
                blkerr2_th,
            ) = ev_sim(
                num_runs=num_runs,
                frequency=combo.frequency,
                num_events=combo.num_events,
                num_bits=combo.num_bits,
                info_bits=combo.info_bits,
                power=combo.power,
                distance=combo.distance,
                N0=combo.N0,
                num_bits_2=combo.num_bits_2,
                info_bits_2=combo.info_bits_2,
                power_2=combo.power_2,
                distance_2=combo.distance_2,
                N0_2=combo.N0_2,
                seed=seed,
            )

            results.append(
                {
                    "frequency": combo.frequency,
                    "num_events": combo.num_events,
                    "num_bits": combo.num_bits,
                    "info_bits": combo.info_bits,
                    "power": combo.power,
                    "distance": combo.distance,
                    "N0": combo.N0,
                    "num_bits_2": (
                        combo.num_bits if combo.num_bits_2 is None else combo.num_bits_2
                    ),
                    "info_bits_2": (
                        combo.info_bits
                        if combo.info_bits_2 is None
                        else combo.info_bits_2
                    ),
                    "power_2": combo.power if combo.power_2 is None else combo.power_2,
                    "distance_2": (
                        combo.distance if combo.distance_2 is None else combo.distance_2
                    ),
                    "N0_2": combo.N0 if combo.N0_2 is None else combo.N0_2,
                    "aaoi_theory": aaoi_th,
                    "aaoi_sim": aaoi_sim,
                    "snr1_avg": snr1_avg,
                    "snr2_avg": snr2_avg,
                    "blkerr1_th": blkerr1_th,
                    "blkerr2_th": blkerr2_th,
                }
            )

        except _SimParamError as spe:
            # In case of invalid parameters or parameter combinations, log the
            # error and proceed to the next combination
            err_msg = str(spe)
            if err_msg not in param_error_log:
                param_error_log[err_msg] = []
            cast(MutableSequence, param_error_log[err_msg]).append(combo)

        if counter is not None:
            counter.value += 1
        if stop_event is not None and stop_event.is_set():
            break

    return pd.DataFrame(results), param_error_log
