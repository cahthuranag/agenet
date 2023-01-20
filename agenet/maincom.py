import numpy as np
import math
import argparse
import random
#import sys
from scipy import special as sp
import av_age
#from av_age import validate
import matplotlib.pyplot as plt
import bler 
import snr
import pandas as pd
import tabulate as tab
import itertools as intert

#%run -i av_age.py 
def main(num_nodes,active_prob):
 lambda1 = 200
 #lambda1 = genlambda[j]
 num_events = 200
 inter_arrival_times=(1/lambda1)*(np.ones(num_events))
 arrival_timestamps = np.cumsum(inter_arrival_times)
 T=10**-4
 N0=2*(10**-15)
 d1=700 # disatance
 d2=700
 P1=10*(10**-4)
 P2=10*(10**-4)
 n=300
 n1=150
 n2=150
 k1=100
 k2=100
 snr1=snr.snr(N0, d1, P1)
 snr2=snr.snr(N0, d2, P2)
 er1=bler.blercal(snr1, n1, k1)
 er2=bler.blercal(snr2, n2, k2)
 inter_service_times = (1/lambda1)* np.ones((num_events))
 #Generating departure timestamps for the node 1
 server_timestamps_1 = np.zeros(num_events)
 departure_timestamps_s = np.zeros(num_events)
 for i  in range (0,num_events):
     su_p = active_prob * (1 - er1) * ((1 - active_prob) **(num_nodes))
     er_f = 1 - su_p
     er_p = er_f + (er2 * (er_f - 1))
     er_indi = int(random.random() > er_p)
     if er_indi == 0:
         departure_timestamps_s[i] = 0
         server_timestamps_1[i] = 0
         
     else:
         departure_timestamps_s[i] = arrival_timestamps[i] + inter_service_times[i]
         server_timestamps_1[i] = arrival_timestamps[i]
 #print(departure_timestamps_1,server_timestamps_1)    
 dep = [x for x in departure_timestamps_s if x != 0]
 sermat = [x for x in server_timestamps_1 if x != 0]
 
 av_age_poisson_simulation,_,_ = av_age.av_age_func(sermat,dep)
 if er_p == 1:
     print("Theoretical average age is not defined")
 else:
  av_age_poisson_theoretical= (1/lambda1) * (0.5 + (1 / (1 - er_p)))
 
 #print(av_age_poisson_simulation,av_age_poisson_theoretical) 
 return av_age_poisson_theoretical,av_age_poisson_simulation