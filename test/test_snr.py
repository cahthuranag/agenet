import math

import pytest

from agenet.snr import snr, snr_th


def test_snr():
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    result = snr(N0, d, P)
    assert isinstance(result, float)
    assert result >= 0


def test_snr_th():
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    result = snr(N0, d, P)
    assert isinstance(result, float)
    assert result >= 0
