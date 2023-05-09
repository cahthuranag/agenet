def snr(N0, d, P):
    """
    Calculates the signal-to-noise ratio (SNR) of the received signal.

    Args:
        N0 (float): The power spectral density of the noise.
        d (float): The distance between the transmitter and receiver.
        P (float): The power of the transmitted signal.

    Returns:
        float: The SNR of the received signal in linear scale.

    """
    import math
    import numpy as np

    f = 6 * (10**9)  # frequency of the signal
    C = 3 * (10**8)  # speed of light
    log_alpha = (20 * math.log10(d)) + (
        20 * math.log10((4 * f * math.pi) / C)
    )  # path loss in dB
    alpha = 1 / (10 ** ((log_alpha) / 10))  # path loss in linear scale
    snr = (alpha * P * np.random.exponential(1)) / N0  #
    return snr


def snr_th(N0, d, P):
    """
    Calculates the theoretical signal-to-noise ratio (SNR) of the received signal.

    Args:
        N0 (float): The power spectral density of the noise.
        d (float): The distance between the transmitter and receiver.
        P (float): The power of the transmitted signal.

    Returns:
        float: The theoretical SNR of the received signal in linear scale.

    """
    import math
    import numpy as np

    f = 6 * (10**9)  # frequency of the signal
    C = 3 * (10**8)  # speed of light
    log_alpha = (20 * math.log10(d)) + (
        20 * math.log10((4 * f * math.pi) / C)
    )  # path loss in dB
    alpha = 1 / (10 ** ((log_alpha) / 10))  # path loss in linear scale
    snr_th = (alpha * P) / N0  #
    return snr_th
