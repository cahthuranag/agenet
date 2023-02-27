import math
import numpy as np
import scipy.special as sp

# this function claculate block error rate for the given snr, n, k
# this function is used in the maincom.py file
# n is the number of bits in the block
# k is the number of bits in the message
# snr is the signal to noise ratio


def qfunc(x):
    if x < 0:
        return 0
    return 0.5 - 0.5 * sp.erf(
        x / math.sqrt(2)
    )  # this function is the q function # this function is the q function


# The Q-function is a mathematical function that gives the tail probability of the standard normal distribution.


# Calculate the BLER for the given SNR, n, k
def blercal(snr, n, k):
    if snr < 0:
        raise ValueError(
            "SNR must be non-negative"
        )  # testing the snr value is non-negative
    if n <= 0:
        raise ValueError(
            "n must be greater than 0"
        )  # testing the n value is greater than 0
    if k <= 0:
        raise ValueError(
            "k must be greater than 0"
        )  # testing the k value is greater than 0

    c = math.log2(1 + snr)  # this is the capacity of the channel
    v = (
        0.5 * (1 - (1 / (1 + snr) ** 2)) * ((math.log2(math.e)) ** 2)
    )  # this is the variance of the channel
    err = qfunc(((n * c) - k) / math.sqrt(n * v))

    return err
