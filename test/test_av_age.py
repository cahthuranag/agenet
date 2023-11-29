import os
import subprocess
import sys

import numpy as np
import pytest
from matplotlib import pyplot as plt

from agenet import av_age_fn


# def test_av_age_func_values():
#     assert av_age_func([2,3,4,5], [1,2,3,4]) == 1.3
@pytest.mark.parametrize(
    "v,T, expected", [([2, 3, 4, 5], [1, 2, 3, 4], 1.3)]
)
def test_av_age_func_values(v, T, expected):
    age, _, _ = av_age_fn(v, T, 0.1)
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


def test_av_age_fn():
    # Define the expected average age of information for the example
    expected_average_age = 1.3
    # Calculate the actual average age of information for the example
    destination_times = [2, 3, 4, 5]
    generation_times = [1, 2, 3, 4]
    lambha = 0.1
    actual_average_age, _, _ = av_age_fn(
        destination_times, generation_times, lambha
    )
    # Check that the actual average age of information
    # matches the expected value
    assert np.isclose(actual_average_age, expected_average_age, rtol=1e-1)


def test_command_line_arguments():
    # Define sample command-line arguments

    dest_times = [0.5, 1.5, 2.5, 3.5, 4.5]
    gen_times = [0.3, 0.8, 1.2, 1.6, 2.0]
    lambha = 1

    # Convert lists to strings
    dest_times_str = " ".join(map(str, dest_times))
    gen_times_str = " ".join(map(str, gen_times))

    script_path = os.path.abspath("agenet/av_age.py")
    # Run the script with the sample command-line arguments
    command = f"python {script_path} --lambha {lambha} --dest_times {dest_times_str} --gen_times {gen_times_str}"
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )

    assert "Average Age of Information:" in result.stdout
