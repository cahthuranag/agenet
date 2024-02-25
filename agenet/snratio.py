"""Signal-to-noise ratio (SNR) calculator."""
import math

import numpy as np


def snr(N0: float, d: float, P: float, fr: float) -> float:
    """Computes the SNR of the received signal.

    Args:
      N0: The power spectral density of the noise.
      d: The distance between the transmitter and receiver.
      P: The power of the transmitted signal.
      fr: The frequency of the signal.

    Returns:
      The SNR of the received signal in linear scale.
    """
    alpha = _alpha(d, fr)
    snr: float = (alpha * P * np.random.exponential(1)) / N0
    return snr


def snr_th(N0: float, d: float, P: float, fr: float) -> float:
    """Calculates the theoretical SNR of the received signal.

    Args:
      N0: The power spectral density of the noise.
      d: The distance between the transmitter and receiver.
      P: The power of the transmitted signal.
      fr: The frequency of the signal.

    Returns:
      The theoretical SNR of the received signal in linear scale.
    """
    alpha = _alpha(d, fr)
    snr_th: float = (alpha * P) / N0
    return snr_th


def _alpha(d: float, fr: float) -> float:
    """Calculates the path loss in linear scale.

    Args:
      d: The distance between the transmitter and receiver.

    Returns:
      The path loss in linear scale.
    """
    f = fr  # frequency of the signal
    C: float = 3 * (10**8)  # speed of light
    log_alpha: float = (20 * math.log10(d)) + (
        20 * math.log10((4 * f * math.pi) / C)
    )  # path loss in dB
    alpha: float = 1 / (10 ** ((log_alpha) / 10))  # path loss in linear scale
    return alpha
