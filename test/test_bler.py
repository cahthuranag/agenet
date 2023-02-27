import math
import numpy as np
import scipy.special as sp
import pytest
from agenet.bler import blercal


def test_blercal():
    # Test case 1: Check the result of the function
    snr = 10
    n = 1000
    k = 500
    result = blercal(snr, n, k)
    assert (
        result >= 0 and result <= 1
    ), f"Expected a value between 0 and 1, but got {result}"

    # Test case 2: Check the result of the function
    snr = 5
    n = 100
    k = 50
    result = blercal(snr, n, k)
    assert (
        result >= 0 and result <= 1
    ), f"Expected a value between 0 and 1, but got {result}"

    # Test case 3: Check the result of the function
    snr = 20
    n = 500
    k = 250
    result = blercal(snr, n, k)
    assert (
        result >= 0 and result <= 1
    ), f"Expected a value between 0 and 1, but got {result}"

    # Test case 4: Check input validation for snr
    snr = -5
    n = 100
    k = 50
    with pytest.raises(ValueError) as e_info:
        blercal(snr, n, k)
    assert str(e_info.value) == "SNR must be non-negative"


# Test case 5: Check input validation for n
snr = 10
n = 0
k = 50
with pytest.raises(ValueError) as e_info:
    result = blercal(snr, n, k)
assert (
    str(e_info.value) == "n must be greater than 0"
), f"Expected 'n must be greater than 0', but got {e_info.value}"

# Test case 6: Check input validation for k
snr = 10
n = 100
k = 0
with pytest.raises(ValueError) as e_info:
    result = blercal(snr, n, k)
assert (
    str(e_info.value) == "k must be greater than 0"
), f"Expected 'k must be greater than 0', but got {e_info.value}"
