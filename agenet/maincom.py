import numpy as np
import math
import argparse
#import sys
import agewire
from scipy import special as sp
from agewire import av_age
#from av_age import validate
import matplotlib.pyplot as plt
import pandas as pd
import tabulate as tab
import itertools as intert

#%run -i av_age.py 
def qfunc(x):
    return 0.5-0.5*sp.erf(x/math.sqrt(2))
 
def main (): 
 
 #genlambda=[200, 400 ,600, 800, 1000]
 genlambda=list(intert.chain(range (7,10,1),range(10,100,1),range(100,200,10)))
 av_age_poisson_simulation = np.zeros(np.size(genlambda))
 av_age_poisson_theoretical = np.zeros(np.size(genlambda))
 for j in range(0,len(genlambda)):
     lambda1 = genlambda[j]
     num_events = 300
     inter_arrival_times=(1/lambda1)*(np.log(1/np.random.rand(num_events)))
     inter_arrival_times_1=  np.delete(inter_arrival_times,-1)
     arrival_timestamps = np.append((np.zeros(1)), (np.cumsum(inter_arrival_times_1)))
     nu_sim_1=10
     service=np.zeros(nu_sim_1)
     for ii in range(0,len(service)):
         nu_sim=1000
         era=np.empty(nu_sim)
 
         for sim in range (0, (nu_sim)):
             f=6*(10**9)
             C=3*(10**8)
             T=10**-4
             N0=2*(10**-15)
             d1=700 # disatance
             d2=700
             P1=1*(10**-4)
             P2=1*(10**-4)
             log_alpha_1=(20*math.log10(d1))+(20*math.log10((4*f*math.pi)/C))
             log_alpha_2=(20*math.log10(d2))+(20*math.log10((4*f*math.pi)/C))
             alpha_1=1/(10**((log_alpha_1)/10))
             alpha_2=1/(10**((log_alpha_2)/10))
             snr1=(alpha_1*P1*np.random.exponential(1))/N0 
             snr2=(alpha_2*P2*np.random.exponential(1))/N0
             n=300
             n1=150
             n2=150
             k1=100
             k2=100
             c1=math.log2(1+snr1)
             v1=0.5*(1-(1/(1+snr1)**2))*((math.log2(np.random.exponential(1)))**2)
             c2=math.log2(1+snr2)
             v2=0.5*(1-(1/(1+snr2)**2))*((math.log2(np.random.exponential(1)))**2)
             er1=qfunc(((n1*c1)-k1)/math.sqrt(n1*v1))
             er2=qfunc(((n2*c2)-k2)/math.sqrt(n2*v2))
             er=er1+(er2*(1-er1))
             #era[sim]==er
             era[sim]=er
         #iii+=1
         erf=np.mean(era)
         service[ii]=(np.random.geometric(1-erf)+1)
     s=T*n/((1-erf))
     inter_service_times_1=s*np.log(1./np.random.rand(num_events))
     #Generating departure timestamps for the node 1
     server_timestamps_1 = np.zeros(num_events)
     departure_timestamps_1 = np.zeros(num_events)
     waiting_timestamps_1=np.zeros(num_events)
     arr_square=np.zeros(num_events)
     arr_square[0]=inter_arrival_times[0]**2
     ser_square=np.zeros(num_events)
     ser_square[0]=inter_service_times_1[0]**2
     server_timestamps_1[0] = 0
     departure_timestamps_1[0] = server_timestamps_1[0] + inter_service_times_1[0]
     for k  in range (1,num_events):
                     if arrival_timestamps[k] < departure_timestamps_1[k-1]:
                      server_timestamps_1[k]= departure_timestamps_1[k-1]
                     else:
                      server_timestamps_1[k] = arrival_timestamps[k]
                     departure_timestamps_1[k] = server_timestamps_1[k] + inter_service_times_1[k]
                     waiting_timestamps_1[k]=departure_timestamps_1[k]-arrival_timestamps[k]-inter_service_times_1[k]
                     arr_square[k]=inter_arrival_times[k]**2
                     ser_square[k]=(inter_service_times_1[k])**2
 
     av_age_poisson_simulation[j],_,_ = av_age.av_age_func(departure_timestamps_1, arrival_timestamps)
     av_age_poisson_theoretical[j]=  np.mean((0.5*np.mean(arr_square)/np.mean(inter_arrival_times))+np.mean(inter_service_times_1)+(np.mean(waiting_timestamps_1*inter_arrival_times)/np.mean(inter_arrival_times)))
     #print(av_age_poisson_simulation)
     
 

 
 #all_data_age=list(zip(genlambda,av_age_poisson_simulation,av_age_poisson_theoretical))
 
#  print(tab.tabulate(all_data_age, tablefmt='psql', showindex=False,
#                          headers=['Update generation rate', 'AAoI simulated',
#                                      'AAoI theoritical']
#                                      ))
 return  genlambda,av_age_poisson_simulation,av_age_poisson_theoretical


def printval():
 from agewire import maincom
 genlambda,av_age_poisson_simulation,av_age_poisson_theoretical=maincom.main()
 all_data_age=list(zip(genlambda,av_age_poisson_simulation,av_age_poisson_theoretical))
 print(tab.tabulate(all_data_age, tablefmt='psql', showindex=False,
                         headers=['Update generation rate', 'AAoI simulated',
                                     'AAoI theoritical']
                                     ))
 
                                
def ageplot ():  
 from agewire import maincom
 #from scipy.interpolate import spline
 from scipy.interpolate import make_interp_spline, BSpline
 genlambda,av_age_poisson_simulation,av_age_poisson_theoretical=maincom.main()
 xnew = np.linspace(np.array(genlambda).min(), np.array(genlambda).max(), 300)  
 spl_sim = BSpline(genlambda, av_age_poisson_simulation, k=2)  # type: BSpline
 sim_smooth = spl_sim(xnew)
 spl_th = BSpline(genlambda, av_age_poisson_theoretical, k=2)  # type: BSpline
 th_smooth = spl_th(xnew)
#  sim_smooth = bpline(genlambda, av_age_poisson_simulation, xnew)
#  th_smooth = spline(genlambda, av_age_poisson_theoretical, xnew)
 plt.plot(xnew,sim_smooth, label='simulated')
 plt.plot(xnew,th_smooth, label='theoretical') 
 plt.xlabel("Update generation rate")
 plt.ylabel("AAoI")
 plt.legend()
 plt.show() 

""" if args.plot: 
 genlambda,av_age_poisson_simulation,av_age_poisson_theoretical=maincom.main()
 plt.plot(genlambda,av_age_poisson_simulation)
 plt.plot(genlambda,av_age_poisson_theoretical) 
 plt.show()  """





            



    
            
        
       