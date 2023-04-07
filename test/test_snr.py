import pytest
import numpy as np

# Importing the function to be tested
from agenet.snr import snr, snr_th

# Define test cases
@pytest.mark.parametrize(
    "N0, d, P, expected",
    [
        (1, 1, 1, snr_th(1, 1, 1)),
        (10, 5, 2, snr_th(10, 5, 2)),
        (100, 10, 5, snr_th(100, 10, 5)),
        (1000, 20, 10, snr_th(1000, 20, 10)),
    ],
)
def test_snr(N0, d, P, expected):
    # Call the function
    result = snr(N0, d, P)

    # Check that the result is within 10% of the expected value
    assert np.isclose(result, expected, rtol=0.1)


@pytest.mark.parametrize(
    "N0, d, P, expected",
    [
        (1, 1, 1, snr_th(1, 1, 1)),
        (10, 5, 2, snr_th(10, 5, 2)),
        (100, 10, 5, snr_th(100, 10, 5)),
        (1000, 20, 10, snr_th(1000, 20, 10)),
    ],
)
def test_snr_th(N0, d, P, expected):
    # Call the function
    result = snr_th(N0, d, P)

    # Check that the result is within 10% of the expected value
    assert np.isclose(result, expected, rtol=0.1)
