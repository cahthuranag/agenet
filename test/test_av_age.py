import numpy as np
import pytest
from scipy.integrate import trapz

from agenet.av_age import average_age_of_information_fn


# def test_av_age_func_values():
#     assert av_age_func([2,3,4,5], [1,2,3,4]) == 1.3
@pytest.mark.parametrize("v,T, expected", [([2, 3, 4, 5], [1, 2, 3, 4], 1.3)])
def test_av_age_func_values(v, T, expected):
    age, _, _ = average_age_of_information_fn(v, T, 0.1)
    assert round(age, 1) == expected


@pytest.fixture(scope="function")
def plot_fn():
    def _plot(points):
        plt.plot(points)
        yield plt.show()
        plt.close("all")

    return _plot


def test_plot_fn(plot_fn):
    points = [1, 2, 3]
    plot_fn(points)
    assert True


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_average_age_of_information_fn():
    # Define the expected average age of information for the example
    expected_average_age = 1.3
    # Calculate the actual average age of information for the example
    destination_times = [2, 3, 4, 5]
    generation_times = [1, 2, 3, 4]
    lambha = 0.1
    actual_average_age, _, _ = average_age_of_information_fn(
        destination_times, generation_times, lambha
    )
    # Check that the actual average age of information matches the expected value
    assert np.isclose(actual_average_age, expected_average_age, rtol=1e-1)


def test_average_age():
    age = [25, 30, 35, 40]
    times = [0, 2, 4, 6]
    average_age = trapz(age, times) / np.amax(times)
    assert np.isclose(average_age, 33.75, rtol=1e-1)
