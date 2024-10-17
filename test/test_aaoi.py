"""Tests for the average age of information function."""

import numpy as np
import pytest

from agenet import aaoi_fn


@pytest.mark.parametrize("v, T, expected", [([2, 3, 4, 5], [1, 2, 3, 4], 1.3)])
def test_av_age_func_values(v, T, expected):
    """Test the aaoi_fn() function."""
    aaoi, _, _ = aaoi_fn(v, T)
    assert round(aaoi, 1) == expected
    assert np.isclose(aaoi, expected, rtol=1e-1)
