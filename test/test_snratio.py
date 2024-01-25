"""Tests for the snr module."""
import os
import subprocess

from agenet import snr


def test_snr():
    """Test the snr function for some known inputs and expected outputs."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    result = snr(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0


def test_snr_th():
    """Test the snr_th function for some known inputs and expected outputs."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    result = snr(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0



