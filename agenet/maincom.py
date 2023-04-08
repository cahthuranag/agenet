import numpy as np
import math
import argparse
import random


# import sys
from scipy import special as sp


# from av_age import validate
import matplotlib.pyplot as plt
from agenet.bler import blercal, blercal_th
import agenet.snr as snr
import agenet.av_age as av_age
import pandas as pd
import tabulate as tab
import itertools as intert
import matplotlib.pyplot as plt


def main(num_nodes, active_prob, n, k, P, numevents):
    lambda1 = 1  # arrival for one transmission period
    # lambda1 = genlambda[j]
    num_events = numevents  # number of events
    inter_arrival_times = (1 / lambda1) * (np.ones(num_events))  # inter arrival times
    arrival_timestamps = np.cumsum(inter_arrival_times)  # arrival timestamps
    N0 = 1 * (10**-13)  # noise power
    d1 = 700  # disatance between the source nodes and the relay or access point
    d2 = 700  # distance between the the relay or access point and the destination
    P1 = P  # power of the source nodes
    P2 = P  # power of the relay or access point
    # n = 300
    n1 = n  # number of bits in the block for the source nodes
    n2 = n  # number of bits in the block for the relay or access point
    k1 = k  # number of bits in the message for the source nodes
    k2 = k  # number of bits in the message for the relay or access point
    # block error rate for the relay or access point at the destination
    snr1_th = snr.snr_th(N0, d1, P1)
    snr2_th = snr.snr_th(N0, d2, P2)
    er1_th = blercal_th(snr1_th, n1, k1)
    er2_th = blercal_th(snr2_th, n2, k2)
    inter_service_times = (1 / lambda1) * np.ones((num_events))  # inter service times
    # Generating departure timestamps for the node 1
    server_timestamps_1 = np.zeros(num_events)
    departure_timestamps_s = np.zeros(num_events)
    su_p_th = active_prob * (1 - er1_th) * ((1 - active_prob) ** (num_nodes - 1))
    er_f_th = 1 - su_p_th
    er_p_th = er_f_th + (er2_th * (er_f_th - 1))
    for i in range(0, num_events):
        snr1 = snr.snr(
            N0, d1, P1
        )  # snr for the source nodes at the relay or access point
        snr2 = snr.snr(N0, d2, P2)
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

    # print(er1, er2, er1_th, er2_th)
    av_age_theoretical = (1 / lambda1) * (0.5 + (1 / (1 - er_p_th)))

    # print(av_age_simulation, av_age_theoretical)
    return av_age_theoretical, av_age_simulation

    # run the main function serveral times and get the average of the results


# This function is used to run the main function several times and get the average of the results
def run_main(num_nodes, active_prob, n, k, P, numevnts, numruns):
    num_runs = numruns  # number of runs
    av_age_theoretical_run = 0
    av_age_simulation_run = 0
    for i in range(num_runs):
        av_age_theoretical_i, av_age_simulation_i = main(
            num_nodes, active_prob, n, k, P, numevnts
        )
        av_age_theoretical_run += av_age_theoretical_i
        av_age_simulation_run += av_age_simulation_i
    av_age_theoretical_run /= num_runs  # average of the theoretical results
    av_age_simulation_run /= num_runs  # average of the simulation results
    return (
        av_age_theoretical_run,
        av_age_simulation_run,
    )  # return the average of the results
