"""Tests for the snr module."""

import pytest
from agenet import snr, snr_th

def test_snr():
    """Test the snr function for some known inputs and expected outputs."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    result = snr(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0

def test_snr_with_seed():
    """Test the snr function with a specific seed."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    seed = 42
    result = snr(N0, d, P, fr, seed=seed)
    assert isinstance(result, float)
    assert result >= 0

def test_snr_reproducibility():
    """Test that snr function produces the same result with the same seed."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    seed = 42
    result1 = snr(N0, d, P, fr, seed=seed)
    result2 = snr(N0, d, P, fr, seed=seed)
    assert result1 == result2

def test_snr_different_seeds():
    """Test that snr function produces different results with different seeds."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    result1 = snr(N0, d, P, fr, seed=42)
    result2 = snr(N0, d, P, fr, seed=43)
    assert result1 != result2

def test_snr_th():
    """Test the snr_th function for some known inputs and expected outputs."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    result = snr_th(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0

def test_snr_th_deterministic():
    """Test that snr_th function always produces the same result for the same inputs."""
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr = 6 * (10**9)
    result1 = snr_th(N0, d, P, fr)
    result2 = snr_th(N0, d, P, fr)
    assert result1 == result2

@pytest.mark.parametrize("N0,d,P,fr", [
    (1e-13, 1000, 1e-3, 6e9),
    (2e-13, 500, 2e-3, 5e9),
    (5e-14, 2000, 5e-4, 7e9),
])
def test_snr_multiple_inputs(N0, d, P, fr):
    """Test snr function with multiple input combinations."""
    result = snr(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0

@pytest.mark.parametrize("N0,d,P,fr", [
    (1e-13, 1000, 1e-3, 6e9),
    (2e-13, 500, 2e-3, 5e9),
    (5e-14, 2000, 5e-4, 7e9),
])
def test_snr_th_multiple_inputs(N0, d, P, fr):
    """Test snr_th function with multiple input combinations."""
    result = snr_th(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0

def test_snr_seed_type_check():
    """Test that snr function raises TypeError for invalid seed type."""
    with pytest.raises(TypeError):
        snr(1e-13, 1000, 1e-3, 6e9, seed="invalid")

def test_snr_negative_seed():
    """Test that snr function raises ValueError for negative seeds."""
    with pytest.raises(ValueError, match="expected non-negative integer"):
        snr(1e-13, 1000, 1e-3, 6e9, seed=-42)

def test_snr_zero_seed():
    """Test that snr function handles zero seed."""
    result = snr(1e-13, 1000, 1e-3, 6e9, seed=0)
    assert isinstance(result, float)
    assert result >= 0

def test_snr_none_seed():
    """Test that snr function works with None seed."""
    result = snr(1e-13, 1000, 1e-3, 6e9, seed=None)
    assert isinstance(result, float)
    assert result >= 0