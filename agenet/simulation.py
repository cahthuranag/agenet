"""Main file for the communication system simulation."""

from __future__ import annotations

from multiprocessing.sharedctypes import Synchronized
from threading import Event

import numpy as np
import pandas as pd
from numpy.random import PCG64, PCG64DXSM, Generator, Philox

from .aaoi import aaoi_fn
from .blkerr import block_error, block_error_th
from .snratio import snr, snr_av


def sim(
    num_bits: int,
    info_bits: int,
    power: float,
    distance: float,
    N0: float,
    frequency: float,
    num_events: int,
    seed: int | np.signedinteger | None = None,
) -> tuple[float, float]:
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
       Theoretical AAoI and simulation AAoI.
    """
    # Input validation

    if num_bits <= 0:
        raise ValueError("n must be greater than 0")
    if info_bits <= 0:
        raise ValueError("k must be greater than 0")
    if info_bits > num_bits:
        raise ValueError("k must be less than or equal to n")
    if power <= 0:
        raise ValueError("P must be greater than 0")
    if N0 <= 0:
        raise ValueError("N0 must be greater than 0")
    if frequency <= 0:
        raise ValueError("fr must be greater than 0")

    # Initialize PCG64 generator
    rng = Generator(PCG64(seed))

    lambda1 = 1  # arrival for one transmission period
    inter_arrival_times = (1 / lambda1) * (np.ones(num_events))  # inter arrival times
    arrival_timestamps = np.cumsum(inter_arrival_times)  # arrival timestamps
    d1 = distance  # distance between source nodes and relay
    d2 = distance  # distance between the relay and destination
    P1 = power  # power of the source nodes
    P2 = power  # power of the relay or access point
    n1 = num_bits  # number of bits in the block for the source nodes
    n2 = num_bits  # number of bits in the block for the relay or access point
    k1 = info_bits  # number of bits in the message for the source nodes
    k2 = info_bits  # number of bits in the message for the relay or access point
    snr1_th = snr_av(
        N0, d1, P1, frequency
    )  # block error rate for the relay or access point at the destination
    snr2_th = snr_av(
        N0, d2, P2, frequency
    )  # block error rate for the source nodes at the relay or access point

    er1_th = block_error_th(snr1_th, n1, k1)
    er2_th = block_error_th(snr2_th, n2, k2)
    inter_service_times = (1 / lambda1) * np.ones((num_events))  # inter service times
    server_timestamps_1 = np.zeros(
        num_events
    )  # Generating departure timestamps for the node 1
    departure_timestamps_s = np.zeros(num_events)
    er_p_th = er1_th + (er2_th * (1-er1_th))
    for i in range(0, num_events):
        snr1 = snr(
            N0, d1, P1, frequency, seed=rng.integers(0, 2**32)
        )  # snr for the source nodes at the relay or access point
        snr2 = snr(N0, d2, P2, frequency, seed=rng.integers(0, 2**32))
        er1 = block_error(
            snr1, n1, k1
        )  # block error rate for the source nodes at the relay or access point
        er2 = block_error(
            snr2, n2, k2
        )  # block error rate for the relay or access point at the destination
        er_p = er1 + (er2 * (1-er1))
        er_indi = int(rng.random() > er_p)  # Using PCG64 generator here
        if er_indi == 0:
            departure_timestamps_s[i] = 0
            server_timestamps_1[i] = 0
        else:
            departure_timestamps_s[i] = arrival_timestamps[i] + inter_service_times[i]
            server_timestamps_1[i] = arrival_timestamps[i]

    dep = [x for x in departure_timestamps_s if x != 0]
    sermat = [x for x in server_timestamps_1 if x != 0]
    depcop = dep.copy()
    if server_timestamps_1[-1] == 0:
        if len(depcop) != 0:
            depcop.pop()
            maxt = max(arrival_timestamps[-1], dep[-1])
        else:
            maxt = arrival_timestamps[-1]
        v1 = depcop + [maxt]
    else:
        v1 = dep

    if departure_timestamps_s[0] == 0:
        if len(sermat) != 0:
            t1 = sermat
        else:
            t1 = [0]
    else:
        t1 = [0] + sermat

    # Handle the case where er_p_th is very close to or equal to 1
    if abs(1 - er_p_th) < 1e-20:  # Choose a small threshold
        return float("inf"), float("inf")

    av_age_theoretical = (1 / lambda1) * (0.5 + (1 / (1 - er_p_th)))

    system_time = 1 / lambda1  # system time (time which update in the system)
    av_age_simulation, _, _ = aaoi_fn(v1, t1, system_time)

    return av_age_theoretical, av_age_simulation


def ev_sim(
    num_bits: int,
    info_bits: int,
    power: float,
    distance: float,
    N0: float,
    frequency: float,
    num_events: int,
    num_runs: int,
    seed: int | np.signedinteger | None = None,
) -> tuple[float, float]:
    """Run the simulation `num_runs` times and return the expected value for the
       AAoI.

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
        av_age_theoretical_i, av_age_simulation_i = sim(
            num_bits,
            info_bits,
            power,
            distance,
            N0,
            frequency,
            num_events,
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
    distance: list[float],
    N0: list[float],
    frequency: list[float],
    num_events: list[int],
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
                                            n_val,
                                            k_val,
                                            P_val,
                                            d_val,
                                            N0_val,
                                            fr_val,
                                            num_events_val,
                                            num_runs,
                                            seed=seed_for_param_combo,
                                        )

                                        results.append(
                                            {
                                                "distance": d_val,
                                                "N0": N0_val,
                                                "frequency": fr_val,
                                                "num_events": num_events_val,
                                                "num_bits": n_val,
                                                "info_bits": k_val,
                                                "power": P_val,
                                                "aaoi_theory": aaoi_theory,
                                                "aaoi_sim": aaoi_sim,
                                            }
                                        )

                                        if counter is not None:
                                            counter.value += 1
                                        if (
                                            stop_event is not None
                                            and stop_event.is_set()
                                        ):
                                            return pd.DataFrame(results)

    return pd.DataFrame(results)