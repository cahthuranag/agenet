"""Main file for the communication system simulation."""
from __future__ import annotations

import argparse
import random

import numpy as np

from agenet import av_age_fn, blercal, blercal_th, snr, snr_th


def main(
    num_nodes: int,
    active_prob: float,
    n: int,
    k: int,
    P: float,
    d: int,
    N0: float,
    fr: float,
    numevents: int,
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

    Returns:
       Theoretical AAoI and simulation AAoI.
    """
    lambda1 = 1  # arrival for one transmission period
    num_events = numevents  # number of events
    inter_arrival_times = (1 / lambda1) * (np.ones(num_events))  # inter arrival times
    arrival_timestamps = np.cumsum(inter_arrival_times)  # arrival timestamps
    d1 = d  # disatance between source nodes and relay
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
            N0, d1, P1, fr
        )  # snr for the source nodes at the relay or access point
        snr2 = snr(N0, d2, P2, fr)
        er1 = blercal(
            snr1, n1, k1
        )  # block error rate for the source nodes at the relay or access point
        er2 = blercal(
            snr2, n2, k2
        )  # block error rate for the relay or access point at the destination
        su_p = active_prob * (1 - er1) * ((1 - active_prob) ** (num_nodes - 1))
        er_f = 1 - su_p
        er_p = er_f + (er2 * (er_f - 1))
        er_indi = int(random.random() > er_p)
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

    system_time = 1 / lambda1  # system time (time which update in the system)
    av_age_simulation, _, _ = av_age_fn(v1, t1, system_time)
    av_age_theoretical = (1 / lambda1) * (0.5 + (1 / (1 - er_p_th)))

    return av_age_theoretical, av_age_simulation


def run_main(
    num_nodes: int,
    active_prob: float,
    n: int,
    k: int,
    P: float,
    d: int,
    N0: float,
    fr: float,
    numevnts: int,
    numruns: int,
) -> tuple[float, float]:
    """Run the simulation `numruns` times and return the AAoI.

    Args:
      num_nodes: Number of nodes in the network.
      active_prob: Probability that a node is active in a given time slot.
      n: Number of bits in a block.
      k: Number of bits in a message.
      P: Power of the nodes.
      numevnts: Number of events.
      numruns: Number of times to run the simulation.

    Returns:
      A tuple containing the theoretical AAoI and the simulation AAoI.
    """
    num_runs = numruns
    av_age_theoretical_run = 0.0
    av_age_simulation_run = 0.0
    for _ in range(num_runs):
        av_age_theoretical_i, av_age_simulation_i = main(
            num_nodes, active_prob, n, k, P, d, N0, fr, numevnts
        )
        av_age_theoretical_run += av_age_theoretical_i
        av_age_simulation_run += av_age_simulation_i
    av_age_theoretical_run /= num_runs
    av_age_simulation_run /= num_runs
    return av_age_theoretical_run, av_age_simulation_run


def _parse_args() -> None:
    """Parse command-line arguments and run the simulation."""
    parser = argparse.ArgumentParser(description="AAoI Simulation")
    parser.add_argument(
        "--num_nodes",
        type=int,
        default=2,
        help="Number of nodes in the network",
    )
    parser.add_argument(
        "--active_prob",
        type=float,
        default=0.5,
        help="Probability that a node is active in a given time slot",
    )
    parser.add_argument("--n", type=int, default=200, help="Number of bits in a block")
    parser.add_argument(
        "--k", type=int, default=150, help="Number of bits in a message"
    )
    parser.add_argument("--P", type=float, default=0.1, help="Power of the nodes")
    parser.add_argument("--numevents", type=int, default=1000, help="Number of events")
    parser.add_argument(
        "--numruns",
        type=int,
        default=100,
        help="Number of times to run the simulation",
    )
    parser.add_argument("--d", type=int, default=700, help="Distance between nodes")
    parser.add_argument("--N0", type=float, default=1 * (10**-13), help="Noise power")
    parser.add_argument(
        "--fr",
        type=float,
        default=6 * (10**9),
        help="Frequency of the signal",
    )
    args = parser.parse_args()

    theoretical_aaoi, simulation_aaoi = run_main(
        args.num_nodes,
        args.active_prob,
        args.n,
        args.k,
        args.P,
        args.d,
        args.N0,
        args.fr,
        args.numevents,
        args.numruns,
    )
    print("Theoretical AAoI:", theoretical_aaoi)
    print("Simulation AAoI:", simulation_aaoi)


if __name__ == "__main__":
    _parse_args()
