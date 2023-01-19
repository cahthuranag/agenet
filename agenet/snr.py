def snr(N0, d, P):
 import math
 import numpy as np
 f=6*(10**9)
 C=3*(10**8)
 log_alpha=(20*math.log10(d))+(20*math.log10((4*f*math.pi)/C))
 alpha=1/(10**((log_alpha)/10))
 snr=(alpha*P*np.random.exponential(1))/N0 
 return snr
