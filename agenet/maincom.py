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
import average

import pandas as pd
import tabulate as tab
import itertools as intert
import matplotlib.pyplot as plt


def main(num_nodes, active_prob):
    lambda1 = 1
    # lambda1 = genlambda[j]
    num_events = 10000
    inter_arrival_times = (1 / lambda1) * (np.ones(num_events))
    arrival_timestamps = np.cumsum(inter_arrival_times)
    T = 10**-4
    N0 = 2 * (10**-15)
    d1 = 700  # disatance
    d2 = 700
    P1 = 500 * (10**-2)
    P2 = 500 * (10**-2)
    # n = 300
    n1 = 300
    n2 = 300
    k1 = 100
    k2 = 100
    snr1 = snr.snr(N0, d1, P1)
    snr2 = snr.snr(N0, d2, P2)
    er1 = bler.blercal(snr1, n1, k1)
    er2 = bler.blercal(snr2, n2, k2)
    inter_service_times = (1 / lambda1) * np.ones((num_events))
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
    system_time = 1 / lambda1
    av_age_simulation, _, _ = average.average_age_of_information_fn(v1, t1, system_time)
    print(er1, er2, su_p, er_p)
    if er_p == 1:
        print("Theoretical average age is not defined")
    else:
        av_age_theoretical = (1 / lambda1) * (0.5 + (1 / (1 - er_p)))

    # print(av_age_simulation, av_age_theoretical)
    return av_age_theoretical, av_age_simulation
