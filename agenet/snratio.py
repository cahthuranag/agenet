"""Signal-to-noise ratio (SNR) calculator."""

from __future__ import annotations

import math
from typing import cast

import numpy as np
from numpy.random import Generator


def snr(
    N0: float, d: float, P: float, fr: float, seed: int | Generator | None = None
) -> float:
    """Computes the instantaneous SNR of the received signal.

    Args:
      N0: Noise power in Watts.
      d: The distance between the transmitter and receiver.
      P: The power of the transmitted signal.
      fr: The frequency of the signal.
      seed: Seed for the random number generator or a previously instantied
        random number generator (optional).

    Returns:
      The instantaneous SNR of the received signal in linear scale.
    """
    if isinstance(seed, Generator):
        rng = cast(Generator, seed)
    else:
        rng = Generator(np.random.SFC64(seed))

    # Calculate large-scale gain using _alpha function
    alpha = _alpha(d, fr)

    # Complex channel coefficient (small-scale fading)
    chah = 1 / np.sqrt(2) * (rng.standard_normal() + 1j * rng.standard_normal())

    # Signal gain (combining large-scale and small-scale effects)
    s_gain = alpha * np.abs(chah**2)

    #  Instantaneous SNR
    snr: float = (P * s_gain) / N0
    return snr


def snr_avg(N0: float, d: float, P: float, fr: float) -> float:
    """Computes the average SNR of the received signal.

    Args:
      N0: Noise power in Watts.
      d: The distance between the transmitter and receiver.
      P: The power of the transmitted signal.
      fr: The frequency of the signal.

    Returns:
      The average SNR of the received signal in linear scale.
    """
    alpha = _alpha(d, fr)
    snr_th: float = (alpha * P) / N0
    return snr_th


def _alpha(d: float, fr: float) -> float:
    """Calculates the path loss in linear scale.

    Args:
      d: The distance between the transmitter and receiver.
      fr: The frequency of the signal.

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
