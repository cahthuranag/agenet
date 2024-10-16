"""Functions for calculating the block error."""

import math

import scipy.special as sp


def _qfunc(x: float) -> float:
    """The Q-function gives the tail probability of the std."""
    if x < 0:
        return 1
    return 0.5 - 0.5 * sp.erf(x / math.sqrt(2))  # pylint: disable=E1101


def block_error(snr: float, n: int, k: int) -> float:
    """Calculate the Block Error Rate (BLER) for the given instantaneous  SNR, n, k.

    Args:
        snr (float): Instantaneous signal-to-noise ratio
        n (int): Total number of bits
        k (int): Number of information bits

    Returns:
        float: The Block Error Rate
    """
    c = math.log2(1 + snr)
    v = 0.5 * ((1 - (1 / ((1 + snr) ** 2))) * ((math.log2(math.exp(1))) ** 2))

    # Handle potential division by zero
    if v == 0:
        return 1.0  # Assume worst-case scenario

    err = _qfunc(((n * c) - k) / math.sqrt(n * v))
    return err


def block_error_th(snr_av: float, n: int, k: int) -> float:
    """Calculate the theoretical Block Error Rate for the given average SNR, n, k.

    Args:
        snr_av: Average Signal-to-noise ratio
        n: Total number of bits
        k: Number of information bits

    Returns:
        float: The theoretical Block Error Rate
    """
    try:
        beta = 1 / (2 * math.pi * math.sqrt((2 ** (2 * k / n)) - 1))
    except ValueError:
        return 1.0  # Assume worst-case scenario if we can't calculate beta

    sim_phi = (2 ** (k / n)) - 1
    phi_bas = sim_phi - (1 / (2 * beta * math.sqrt(n)))
    delta = sim_phi + (1 / (2 * beta * math.sqrt(n)))

    err_th = 1 - (
        (beta * math.sqrt(n) * snr_av)
        * (math.exp(-1 * phi_bas * (1 / snr_av)) - math.exp(-1 * delta * (1 / snr_av)))
    )
    return err_th
