import math
import numpy as np
import scipy.special as sp

# this function claculate block error rate for the given snr, n, k
# this function is used in the maincom.py file
# n is the number of bits in the block
# k is the number of bits in the message
# snr is the signal to noise ratio


def qfunc(x):
    return 0.5 - 0.5 * sp.erf(x / math.sqrt(2))  # this function is the q function


# Calculate the BLER for the given SNR, n, k
def blercal(snr, n, k):
    import bler

    c = math.log2(1 + snr)  # this is the capacity of the channel
    v = (
        0.5 * (1 - (1 / (1 + snr) ** 2)) * ((math.log2(math.e)) ** 2)
    )  # this is the variance of the channel
    err = bler.qfunc(((n * c) - k) / math.sqrt(n * v))  # this is the block error rate
    if err < 0:  # if q function give it is considered as 1 as the error rate
        err = 1
    return err  # return the error rate
