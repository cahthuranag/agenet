import math


def blercal_th(snr, n, k):
    beta = 1 / (2 * math.pi * math.sqrt((2 ** (2 * k / n)) - 1))
    sim_phi = (2 ** (k / n)) - 1
    phi_bas = sim_phi - (1 / (2 * beta * math.sqrt(n)))
    delta = sim_phi + (1 / (2 * beta * math.sqrt(n)))
    err_th = 1 - (
        (beta * math.sqrt(n) * snr)
        * (math.exp(-1 * phi_bas * (1 / snr)) - math.exp(-1 * delta * (1 / snr)))
    )
    return err_th
