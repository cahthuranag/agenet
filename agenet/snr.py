# this function calculates the snr of the signal received by the user at the receiver
def snr(N0, d, P):
    import math
    import numpy as np

    f = 6 * (10**9)  # frequency of the signal
    C = 3 * (10**8)  # speed of light
    log_alpha = (20 * math.log10(d)) + (
        20 * math.log10((4 * f * math.pi) / C)
    )  # path loss in dB
    alpha = 1 / (10 ** ((log_alpha) / 10))  # path loss in linear scale
    snr = (alpha * P * np.random.exponential(1)) / N0  #
    return snr  # return snr in linear scale


def snr_th(N0, d, P):
    import math
    import numpy as np

    f = 6 * (10**9)  # frequency of the signal
    C = 3 * (10**8)  # speed of light
    log_alpha = (20 * math.log10(d)) + (
        20 * math.log10((4 * f * math.pi) / C)
    )  # path loss in dB
    alpha = 1 / (10 ** ((log_alpha) / 10))  # path loss in linear scale
    snr_th = (alpha * P) / N0  #
    return snr_th  # return snr in linear scale
