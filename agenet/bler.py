from agenet import maincom
import math 
import numpy as np
import scipy.special as sp

def qfunc(x):
    return 0.5-0.5*sp.erf(x/math.sqrt(2))
#Calculate the BLER for the given SNR, n, k, m.
def blercal(snr, n, k):
 from agenet import bler
 c = math.log2(1 + snr)
 v = 0.5 * (1 - (1 / (1 + snr) ** 2)) * ((math.log2(np.random.exponential(1))) ** 2)
 err = bler.qfunc(((n * c) - k) / math.sqrt(n * v))
 if err<0:
    err=1
 return err