import math
import numpy as np
import scipy.special as sp
import pytest
from agenet.bler import blercal, blercal_th

# Test blercal() function


def test_blercal():
    # Test for non-negative SNR
    with pytest.raises(ValueError, match="SNR must be non-negative"):
        blercal(-1, 100, 50)

    # Test for n > 0
    with pytest.raises(ValueError, match="n must be greater than 0"):
        blercal(10, 0, 50)

    # Test for k > 0
    with pytest.raises(ValueError, match="k must be greater than 0"):
        blercal(10, 100, 0)

    # Test for k <= n
    with pytest.raises(ValueError, match="k must be less than or equal to n"):
        blercal(10, 50, 100)

    # Test for small SNR
    assert np.isclose(blercal(1e-3, 100, 50), 1, rtol=1e-2)

    # Test for large SNR
    assert np.isclose(blercal(100, 100, 50), 0.0, rtol=1e-2)


# Test blercal_th() function


def test_blercal_th():
    # Test for small SNR
    assert np.isclose(blercal_th(1e-6, 300, 280), 1, rtol=1e-1)

    # Test for large SNR
    assert np.isclose(round(blercal_th(1000, 600, 100), 3), 0)
