"""Main file for the communication system simulation."""

from __future__ import annotations

import numpy as np
from numpy.random import PCG64, Generator

from .av_age import av_age_fn
from .bler import blercal, blercal_th
from .snratio import snr, snr_th
import  pandas as pd


def sim(
    num_nodes: int,
    active_prob: float,
    n: int,
    k: int,
    P: float,
    d: float,
    N0: float,
    fr: float,
    numevents: int,
    seed: int | None = None,
) -> tuple[float, float]:
    """Simulates a communication system and calculates the AAoI.

    Args:
      num_nodes: Number of nodes in the system
      active_prob: Probability that a node is active.
      n: Number of bits in a block.
      k: Number of bits in a message.
      P: Power of the nodes.
      d: Distance between nodes.
      N0: Noise power.
      fr: Frequency of the signal.
      numevents: Number of events to simulate.
      seed: Seed for the random number generator (optional).

    Returns:
       Theoretical AAoI and simulation AAoI.
    """
    # Input validation
    if not 0 <= active_prob <= 1:
        raise ValueError("active_prob must be between 0 and 1")
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if k <= 0:
        raise ValueError("k must be greater than 0")
    if k > n:
        raise ValueError("k must be less than or equal to n")
    if P <= 0:
        raise ValueError("P must be greater than 0")
    if N0 <= 0:
        raise ValueError("N0 must be greater than 0")
    if fr <= 0:
        raise ValueError("fr must be greater than 0")

    # Initialize PCG64 generator
    rng = Generator(PCG64(seed))

    lambda1 = 1  # arrival for one transmission period
    num_events = numevents  # number of events
    inter_arrival_times = (1 / lambda1) * (np.ones(num_events))  # inter arrival times
    arrival_timestamps = np.cumsum(inter_arrival_times)  # arrival timestamps
    d1 = d  # distance between source nodes and relay
    d2 = d  # distance between the relay and destination
    P1 = P  # power of the source nodes
    P2 = P  # power of the relay or access point
    n1 = n  # number of bits in the block for the source nodes
    n2 = n  # number of bits in the block for the relay or access point
    k1 = k  # number of bits in the message for the source nodes
    k2 = k  # number of bits in the message for the relay or access point
    snr1_th = snr_th(
        N0, d1, P1, fr
    )  # block error rate for the relay or access point at the destination
    snr2_th = snr_th(
        N0, d2, P2, fr
    )  # block error rate for the source nodes at the relay or access point
    
    er1_th = blercal_th(snr1_th, n1, k1)
    er2_th = blercal_th(snr2_th, n2, k2)
    inter_service_times = (1 / lambda1) * np.ones((num_events))  # inter service times
    server_timestamps_1 = np.zeros(
        num_events
    )  # Generating departure timestamps for the node 1
    departure_timestamps_s = np.zeros(num_events)
    su_p_th = active_prob * (1 - er1_th) * ((1 - active_prob) ** (num_nodes - 1))
    er_f_th = 1 - su_p_th
    er_p_th = er_f_th + (er2_th * (er_f_th - 1))
    for i in range(0, num_events):
        snr1 = snr(
            N0, d1, P1, fr, seed=rng.integers(0, 2**32)
        )  # snr for the source nodes at the relay or access point
        snr2 = snr(N0, d2, P2, fr, seed=rng.integers(0, 2**32))
        er1 = blercal(
            snr1, n1, k1
        )  # block error rate for the source nodes at the relay or access point
        er2 = blercal(
            snr2, n2, k2
        )  # block error rate for the relay or access point at the destination
        su_p = active_prob * (1 - er1) * ((1 - active_prob) ** (num_nodes - 1))
        er_f = 1 - su_p
        er_p = er_f + (er2 * (er_f - 1))
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
    av_age_simulation, _, _ = av_age_fn(v1, t1, system_time)

    return av_age_theoretical, av_age_simulation


def ev_sim(
    num_nodes: int,
    active_prob: float,
    n: int,
    k: int,
    P: float,
    d: float,
    N0: float,
    fr: float,
    numevnts: int,
    numruns: int,
    seed: int | None = None,
) -> tuple[float, float]:
    """Run the simulation `numruns` times and return the AAoI.

    Args:
      num_nodes: Number of nodes in the network.
      active_prob: Probability that a node is active in a given time slot.
      n: Number of bits in a block.
      k: Number of bits in a message.
      P: Power of the nodes.
      d: Distance between nodes.
      N0: Noise power.
      fr: Frequency of the signal.
      numevnts: Number of events.
      numruns: Number of times to run the simulation.
      seed: Seed for the random number generator (optional).

    Returns:
      A tuple containing the theoretical AAoI and the simulation AAoI.
    """
    num_runs = numruns
    av_age_theoretical_run = 0.0
    av_age_simulation_run = 0.0
    rng = Generator(PCG64(seed))  # Initialize RNG here for consistent seeds across runs
    for _ in range(num_runs):
        run_seed = rng.integers(0, 2**32)  # Generate a new seed for each run
        av_age_theoretical_i, av_age_simulation_i = sim(
            num_nodes, active_prob, n, k, P, d, N0, fr, numevnts, seed=run_seed
        )
        if np.isinf(av_age_theoretical_i):
            return float("inf"), float(
                "inf"
            )  # Return infinity for both if theoretical is infinity
        av_age_theoretical_run += av_age_theoretical_i
        av_age_simulation_run += av_age_simulation_i
    av_age_theoretical_run /= num_runs
    av_age_simulation_run /= num_runs
    return av_age_theoretical_run, av_age_simulation_run

def multi_param_ev_sim(
    d: list[float],
    N0: list[float],
    fr: list[float],
    numevnts: list[int],
    num_nodes: list[int],
    active_prob: list[float],
    n: list[int],
    k: list[int],
    P: list[float],
    numruns: int,
    seed: int | None = None,
) -> pd.DataFrame:
    """Run the simulation for multiple parameters and return the results.

    Args:

    d: List of distances between nodes.
    N0: List of noise powers.
    fr: List of frequencies.    
    numevnts: List of number of events.
    num_nodes: List of number of nodes.
    active_prob: List of active probabilities.
    n: List of number of bits in a block.
    k: List of number of bits in a message.
    P: List of powers.
    numruns: Number of times to run the simulation.
    seed: Seed for the random number generator (optional).

    Returns:
    A DataFrame containing the results of the simulation.
    """
    results = []
    
    for d_val in d:
        for N0_val in N0:
            for fr_val in fr:
                for numevnts_val in numevnts:
                    for num_nodes_val in num_nodes:
                        for active_prob_val in active_prob:
                            for n_val in n:
                                for k_val in k:
                                    for P_val in P:
                                        av_age_theoretical, av_age_simulation = ev_sim(
                                            num_nodes_val, active_prob_val, n_val, k_val, 
                                            P_val, d_val, N0_val, fr_val, numevnts_val, 
                                            numruns, seed=seed
                                        )
                                        results.append({
                                            'd': d_val,
                                            'N0': N0_val,
                                            'fr': fr_val,
                                            'numevnts': numevnts_val,
                                            'num_nodes': num_nodes_val,
                                            'active_prob': active_prob_val,
                                            'n': n_val,
                                            'k': k_val,
                                            'P': P_val,
                                            'av_age_theoretical': av_age_theoretical,
                                            'av_age_simulation': av_age_simulation
                                        })
    
    return pd.DataFrame(results)


