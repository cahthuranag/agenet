"""Module containing core communication system simulation."""

from __future__ import annotations

from multiprocessing.sharedctypes import Synchronized
from threading import Event

import numpy as np
import pandas as pd
from numpy import nan
from numpy.random import PCG64, PCG64DXSM, Generator, Philox

from .aaoi import aaoi_fn
from .blkerr import block_error, block_error_th
from .snratio import snr, snr_av


def _sim(
    frequency: float,
    num_events: int,
    num_bits_1: int,
    info_bits_1: int,
    power_1: float,
    distance_1: float,
    n0_1: float,
    blkerr1_th: float,
    num_bits_2: int,
    info_bits_2: int,
    power_2: float,
    distance_2: float,
    n0_2: float,
    blkerr2_th: float,
    rng: Generator,
) -> tuple[float, float]:
    """Low-level function for simulating a communication system and obtaining the AAoI.

    Args:
      TODO

    Returns:
       TODO
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
        snr1 = snr(n0_1, distance_1, power_1, frequency, seed=rng.integers(0, 2**32))
        snr2 = snr(n0_2, distance_2, power_2, frequency, seed=rng.integers(0, 2**32))

        # block error rate for the source nodes at the relay or access point
        er1 = block_error(snr1, num_bits_1, info_bits_1)

        # block error rate for the relay or access point at the destination
        er2 = block_error(snr2, num_bits_2, info_bits_2)

        er_p = er1 + (er2 * (1 - er1))
        er_indi = int(rng.random() > er_p)

        if er_indi == 0:
            # If the packet is not successfully decoded at the destination,
            # departure timestamp is set to nan
            departure_timestamps_s[i] = nan
            server_timestamps_1[i] = nan
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
    if departure_timestamps_s[-1] == nan:
        depature_mat = dep + arrival_timestamps[-1] + inter_service_times[-1]
        arrival_mat = [0] + sermat[1:] + arrival_timestamps[-1]
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
      num_bits: Number of bits in a block ($n$).
      info_bits: Number of bits in a message ($k$).
      power: Transmission power in Watts ($P$).
      distance: Distance between nodes ($d$).
      N0: Noise power in Watts.
      frequency: Signal frequency in Hertz.
      num_events: Number of events to simulate.
      seed: Seed for the random number generator (optional).

    Returns:
       A tuple containing: theoretical AAoI, simulation AAoI, theoretical SNR at
       source node, theoretical SNR at relay or access point, theoretical block
       error at source node, theoretical SNR at relay or access point.
    """
    # Distance between source node and relay
    d1 = distance
    # Distance between the relay and destination
    d2 = distance if distance_2 is None else distance_2
    # Power of the source node
    p1 = power
    # Power of the relay or access point
    p2 = power if power_2 is None else power_2
    # Number of bits in the block for the source node
    n1 = num_bits
    # Number of bits in the block for the relay or access point
    n2 = num_bits if num_bits_2 is None else num_bits_2
    # Number of bits in the message for the source node
    k1 = info_bits
    # Number of bits in the message for the relay or access point
    k2 = info_bits if info_bits_2 is None else info_bits_2
    # Noise power in the source node
    np01 = N0
    # Noise power for the relay or access point
    np02 = N0 if N0_2 is None else N0_2

    # Input validation
    if n1 <= 0 or n2 <= 0:
        raise ValueError("`num_bits` and `num_bits_2` must be greater than 0")
    if k1 <= 0 or k2 <= 0:
        raise ValueError("`info_bits` and `info_bits_2` must be greater than 0")
    if k1 > n1 or k2 > n2:
        raise ValueError("`info_bits` must be less than or equal to `num_bits`")
    if p1 <= 0 or p2 <= 0:
        raise ValueError("`power` and `power_2` must be greater than 0")
    if np01 <= 0 or np02 <= 0:
        raise ValueError("`N0` and `N0_2` must be greater than 0")
    if frequency <= 0:
        raise ValueError("`frequency` must be greater than 0")

    # num_bits_2 >= num_bits_1
    if n1 < n2:
        raise ValueError("`num_bits_2` must be equal or greater than `num_bits`")

    # Initialize PCG64 generator
    rng = Generator(PCG64(seed))

    # Determine the average SNR for the two nodes
    snr1_avg = snr_av(np01, d1, p1, frequency)
    snr2_avg = snr_av(np02, d2, p2, frequency)

    # Block error rate for the relay or access point at the destination
    # TODO: Check above comment for correctness
    er1_th = block_error_th(snr1_avg, n1, k1)

    # Block error rate for the source node at the relay or access point
    # TODO: Check above comment for correctness
    er2_th = block_error_th(snr2_avg, n2, k2)

    # Call the low-level function to actually perform the simulation
    return (
        *_sim(
            frequency=frequency,
            num_events=num_events,
            num_bits_1=n1,
            info_bits_1=k1,
            power_1=p1,
            distance_1=d1,
            n0_1=np01,
            blkerr1_th=er1_th,
            num_bits_2=n2,
            info_bits_2=k2,
            power_2=p2,
            distance_2=d2,
            n0_2=np02,
            blkerr2_th=er2_th,
            rng=rng,
        ),
        snr1_avg,
        snr2_avg,
        er1_th,
        er2_th,
    )


def ev_sim(
    frequency: float,
    num_events: int,
    num_bits: int,
    info_bits: int,
    power: float,
    distance: float,
    N0: float,
    num_runs: int,
    seed: int | np.signedinteger | None = None,
) -> tuple[float, float]:
    """Run the simulation `num_runs` times and return the AAoI expected value.

    Args:
      num_bits: Number of bits in a block.
      info_bits: Number of bits in a message.
      power: Power of the nodes.
      distance: Distance between nodes.
      N0: Noise power.
      frequency: Signal frequency in Hertz.
      num_events: Number of events.
      num_runs: Number of times to run the simulation.
      seed: Seed for the random number generator (optional).

    Returns:
      A tuple containing the expected value for the theoretical AAoI and the
        simulation AAoI.
    """
    ev_age_theoretical_run = 0.0
    ev_age_simulation_run = 0.0

    # Initialize RNG here for consistent seeds across runs
    rng = Generator(PCG64DXSM(seed))

    # Generate a seed for each run
    seeds_for_runs = rng.integers(np.iinfo(np.int64).max, size=num_runs, dtype=np.int64)

    for i in range(num_runs):
        av_age_theoretical_i, av_age_simulation_i, _, _, _, _ = sim(
            frequency,
            num_events,
            num_bits,
            info_bits,
            power,
            distance,
            N0,
            seed=seeds_for_runs[i],
        )
        if np.isinf(av_age_theoretical_i):
            return float("inf"), float(
                "inf"
            )  # Return infinity for both if theoretical is infinity
        ev_age_theoretical_run += av_age_theoretical_i
        ev_age_simulation_run += av_age_simulation_i
    ev_age_theoretical_run /= num_runs
    ev_age_simulation_run /= num_runs
    return ev_age_theoretical_run, ev_age_simulation_run


def multi_param_ev_sim(
    frequency: list[float],
    num_events: list[int],
    distance: list[float],
    N0: list[float],
    num_bits: list[int],
    info_bits: list[int],
    power: list[float],
    num_runs: int,
    seed: int | np.signedinteger | None = None,
    counter: Synchronized[int] | None = None,
    stop_event: Event | None = None,
) -> pd.DataFrame:
    """Run the simulation for multiple parameters and return the results.

    Args:
      distance: List of distances between nodes.
      N0: List of noise powers.
      frequency: List of frequencies.
      num_events: List of number of events.
      num_bits: List of number of bits in a block.
      info_bits: List of number of bits in a message.
      power: List of powers.
      num_runs: Number of times to run the simulation.
      seed: Seed for the random number generator (optional).
      counter: An optional `multiprocessing.Value` which will be incremented
        after each inner loop pass. Only relevant if this function is executed
        in a separate thread.
      stop_event: The simulation will stop if this optional event is set
        externally. Only relevant if this function is executed in a separate
        thread.

    Returns:
      A DataFrame containing the results of the simulation.
    """
    rng = Generator(Philox(seed))

    results = []

    for d_val in distance:
        for N0_val in N0:
            for fr_val in frequency:
                for num_events_val in num_events:
                    for n_val in num_bits:
                        for k_val in info_bits:
                            for P_val in power:
                                seed_for_param_combo = rng.integers(
                                    np.iinfo(np.int64).max, dtype=np.int64
                                )

                                aaoi_theory, aaoi_sim = ev_sim(
                                    fr_val,
                                    num_events_val,
                                    n_val,
                                    k_val,
                                    P_val,
                                    d_val,
                                    N0_val,
                                    num_runs,
                                    seed=seed_for_param_combo,
                                )

                                results.append(
                                    {
                                        "frequency": fr_val,
                                        "num_events": num_events_val,
                                        "distance": d_val,
                                        "N0": N0_val,
                                        "num_bits": n_val,
                                        "info_bits": k_val,
                                        "power": P_val,
                                        "aaoi_theory": aaoi_theory,
                                        "aaoi_sim": aaoi_sim,
                                    }
                                )

                                if counter is not None:
                                    counter.value += 1
                                if stop_event is not None and stop_event.is_set():
                                    return pd.DataFrame(results)

    return pd.DataFrame(results)
