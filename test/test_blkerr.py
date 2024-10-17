"""Tests for the blkerr module."""

import math

import numpy as np
import pytest

from agenet import block_error, block_error_th
from agenet.blkerr import _qfunc


def test_block_error():
    """Test the block_error function for some known inputs and expected outputs."""
    # Test for non-negative SNR
    with pytest.raises(ValueError, match="math domain error"):
        block_error(-1, 100, 50)

    # Test for n > 0
    with pytest.raises(ZeroDivisionError, match="float division by zero"):
        block_error(10, 0, 50)

    # Test for small SNR
    assert np.isclose(block_error(1e-3, 100, 50), 1, rtol=1e-2)

    # Test for large SNR
    assert np.isclose(block_error(100, 100, 50), 0.0, rtol=1e-2)


def test_block_error_th():
    """Test the block_error_th function for some known inputs and expected outputs."""
    # Test for small SNR
    assert np.isclose(block_error_th(1e-6, 300, 280), 1, rtol=1e-1)

    # Test for large SNR
    assert np.isclose(round(block_error_th(1000, 600, 100), 3), 0)


def test_qfunc():
    """Test the qfunc function for some known inputs and expected outputs."""
    # Test the qfunc function for some known inputs and expected outputs
    assert _qfunc(-10) == 1
    assert _qfunc(-1) == 1
    assert _qfunc(0) == 0.5
    assert _qfunc(1) == 0.15865525393145707

    # Test the qfunc function for some edge cases
    assert math.isnan(_qfunc(float("nan")))
    assert _qfunc(float("-inf")) == 1
    assert _qfunc(float("inf")) == 0
