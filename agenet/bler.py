"""Block Error Rate (BLER) Calculation."""

import math

import scipy.special as sp


def _qfunc(x: float) -> float:
    """The Q-function gives the tail probability of the std.

    Args:
      x: input value for Q-function.

    Returns:
      Value of the Q-function evaluated at x.
    """
    if x < 0:
        return 1
    return 0.5 - 0.5 * sp.erf(x / math.sqrt(2))  # pylint: disable=E1101


def blercal(snr: float, n: int, k: int) -> float:
    """Calculate the Block Error Rate (BLER) for the given SNR, n, k.

    Args:
      snr: Signal-to-Noise Ratio (SNR).
      n: Number of bits in the block.
      k: Number of bits in the message.

    Returns:
      Block Error Rate (BLER) for the given SNR, n, k.
    """
    if snr < 0:
        raise ValueError("SNR must be non-negative")
    if n <= 0:
        raise ValueError("n must be greater than 0")
    if k <= 0:
        raise ValueError("k must be greater than 0")
    if k > n:
        raise ValueError("k must be less than or equal to n")
    c = math.log2(1 + snr)
    v = 0.5 * (1 - (1 / (1 + snr) ** 2)) * ((math.log2(math.exp(1))) ** 2)
    err = _qfunc(((n * c) - k) / math.sqrt(n * v))
    return err


def blercal_th(snr: float, n: int, k: int) -> float:
    """Calculate the theoretical Block Error Rate (BLER) for the given SNR, n, k.

    Args:
      snr: Signal-to-Noise Ratio (SNR).
      n: Number of bits in the block.
      k: Number of bits in the message.

    Returns:
      Theoretical Block Error Rate (BLER) for the given SNR, n, k.
    """
    beta = 1 / (2 * math.pi * math.sqrt((2 ** (2 * k / n)) - 1))
    sim_phi = (2 ** (k / n)) - 1
    phi_bas = sim_phi - (1 / (2 * beta * math.sqrt(n)))
    delta = sim_phi + (1 / (2 * beta * math.sqrt(n)))
    err_th = 1 - (
        (beta * math.sqrt(n) * snr)
        * (math.exp(-1 * phi_bas * (1 / snr)) - math.exp(-1 * delta * (1 / snr)))
    )
    return err_th
