import numpy as np
import math
import argparse
import random

# import sys
from scipy import special as sp


# from av_age import validate
import matplotlib.pyplot as plt
import bler
import snr
import av_age
import pandas as pd
import tabulate as tab
import itertools as intert
import matplotlib.pyplot as plt


def main(num_nodes, active_prob, n, k, P):
    lambda1 = 1
    # lambda1 = genlambda[j]
    num_events = 100  # number of events
    inter_arrival_times = (1 / lambda1) * (np.ones(num_events))  # inter arrival times
    arrival_timestamps = np.cumsum(inter_arrival_times)  # arrival timestamps
    N0 = 2 * (10**-15)  # noise power
    d1 = 700  # disatance between the source nodes and the relay or access point
    d2 = 700  # distance between the the relay or access point and the destination
    P1 = P  # power of the source nodes
    P2 = P  # power of the relay or access point
    # n = 300
    n1 = n  # number of bits in the block for the source nodes
    n2 = n  # number of bits in the block for the relay or access point
    k1 = k  # number of bits in the message for the source nodes
    k2 = k  # number of bits in the message for the relay or access point
    snr1 = snr.snr(N0, d1, P1)  # snr for the source nodes at the relay or access point
    snr2 = snr.snr(N0, d2, P2)  # snr for the relay or access point at the destination
    er1 = bler.blercal(
        snr1, n1, k1
    )  # block error rate for the source nodes at the relay or access point
    er2 = bler.blercal(
        snr2, n2, k2
    )  # block error rate for the relay or access point at the destination
    inter_service_times = (1 / lambda1) * np.ones((num_events))  # inter service times
    # Generating departure timestamps for the node 1
    server_timestamps_1 = np.zeros(num_events)
    departure_timestamps_s = np.zeros(num_events)
    su_p = active_prob * (1 - er1) * ((1 - active_prob) ** (num_nodes - 1))
    er_f = 1 - su_p
    er_p = er_f + (er2 * (er_f - 1))
    for i in range(0, num_events):
        er_indi = int(random.random() > er_p)
        if er_indi == 0:
            departure_timestamps_s[i] = 0
            server_timestamps_1[i] = 0

        else:
            departure_timestamps_s[i] = arrival_timestamps[i] + inter_service_times[i]
            server_timestamps_1[i] = arrival_timestamps[i]
    # print(server_timestamps_1,departure_timestamps_s)
    dep = [x for x in departure_timestamps_s if x != 0]
    sermat = [x for x in server_timestamps_1 if x != 0]
    depcop = dep.copy()
    sermat_int = sermat.copy()
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
    # if np.size(dep) == 1 or np.size(sermat) == 1:
    # dep.extend([arrival_timestamps[-1]])
    # sermat= [arrival_timestamps[1]]+ sermat

    # print(sermat, dep)
    system_time = 1 / lambda1  # system time (time which update in the system)
    av_age_simulation, _, _ = av_age.average_age_of_information_fn(v1, t1, system_time)
    print(er1, er2, su_p, er_p)
    if er_p == 1:
        print("Theoretical average age is not defined")
    else:
        av_age_theoretical = (1 / lambda1) * (0.5 + (1 / (1 - er_p)))

    # print(av_age_simulation, av_age_theoretical)
    return av_age_theoretical, av_age_simulation

    # run the main function serveral times and get the average of the results


# This function is used to run the main function several times and get the average of the results
def run_main(num_nodes, active_prob, n, k, P):
    num_runs = 100  # number of runs
    av_age_theoretical_run = 0
    av_age_simulation_run = 0
    for i in range(num_runs):
        av_age_theoretical_i, av_age_simulation_i = main(
            num_nodes, active_prob, n, k, P
        )
        av_age_theoretical_run += av_age_theoretical_i
        av_age_simulation_run += av_age_simulation_i
    av_age_theoretical_run /= num_runs  # average of the theoretical results
    av_age_simulation_run /= num_runs  # average of the simulation results
    return (
        av_age_theoretical_run,
        av_age_simulation_run,
    )  # return the average of the results
