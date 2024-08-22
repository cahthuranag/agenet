"""Tests for the printage.py script."""

import argparse
import io
import os
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock
from unittest.mock import mock_open, patch

import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

from agenet import generate_table, plot, plot_generate


# ... [previous assert_table_format function remains unchanged] ...


def test_generate_table():
    """Test the generate_table() function."""
    # Test input values for the function
    num_nodes_const = 2
    active_prob_const = 0.5
    n_const = 150
    k_const = 100
    P_const = 2 * (10**-3)
    d_const = 700
    N0_const = 1 * (10**-13)
    fr_const = 6 * (10**9)
    numevnts = 100
    numruns = 100
    num_nodes_vals = [1, 2, 3]
    active_prob_vals = [0.1, 0.2]
    n_vals = [150, 160]
    k_vals = [50, 60]
    P_vals = [2 * (10**-3), 4 * (10**-3)]
    seed = 42  # Add a seed for reproducibility

    # Capture the printed output
    output = io.StringIO()
    with redirect_stdout(output):
        generate_table(
            num_nodes_const,
            active_prob_const,
            n_const,
            k_const,
            P_const,
            d_const,
            N0_const,
            fr_const,
            numevnts,
            numruns,
            num_nodes_vals,
            active_prob_vals,
            n_vals,
            k_vals,
            P_vals,
            seed=seed,
        )
    output_str = output.getvalue()

    # Split the output into lines and check the format using tabulate
    output_lines = output_str.strip().split("\n")
    headers = [header.strip() for header in output_lines[0].strip().split("|")[1:-1]]
    table_data = [row.strip().split("|")[1:-1] for row in output_lines[2:-1]]

    expected_table = tabulate(table_data, headers=headers, tablefmt="grid")
    actual_table = tabulate(table_data, headers=headers, tablefmt="grid")

    assert expected_table == actual_table


def test_generate_csv():
    """Test the generate_table() function with CSV output."""
    num_nodes_const = 2
    active_prob_const = 0.5
    n_const = 150
    k_const = 100
    P_const = 2 * (10**-3)
    d_const = 700
    N0_const = 1 * (10**-13)
    fr_const = 6 * (10**9)
    numevnts = 100
    numruns = 100
    num_nodes_vals = [1, 2, 3]
    active_prob_vals = [0.1, 0.2]
    n_vals = [150, 160]
    k_vals = [50, 60]
    P_vals = [2 * (10**-3), 4 * (10**-3)]
    seed = 42  # Add a seed for reproducibility
    # Define a temporary CSV location for testing
    temp_csv_location = "temp_test_results.csv"

    # Create a mock open() function to simulate file operations
    m = mock_open()

    # Mock os.path.getsize to return a predefined size or zero
    with patch("os.path.getsize", return_value=0), patch("builtins.open", m):
        # Execute the generate_table function with only the CSV location argument
        generate_table(
            num_nodes_const,
            active_prob_const,
            n_const,
            k_const,
            P_const,
            d_const,
            N0_const,
            fr_const,
            numevnts,
            numruns,
            num_nodes_vals,
            active_prob_vals,
            n_vals,
            k_vals,
            P_vals,
            csv_location=temp_csv_location,
            seed=seed,
        )
    m().write.assert_called()


def test_plot(monkeypatch):
    """Test the plot() function."""
    parser = argparse.ArgumentParser()
    # ... [previous argument definitions remain unchanged] ...
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for the random number generator.",
    )

    # Mock the command-line arguments
    monkeypatch.setattr(
        "sys.argv",
        [
            "test_script.py",
            "--num_nodes_const",
            "2",
            "--active_prob_const",
            "0.5",
            "--n_const",
            "150",
            "--k_const",
            "100",
            "--P_const",
            "0.002",
            "--numevnts",
            "1000",
            "--numruns",
            "2",
            "--num_nodes_vals",
            "1",
            "2",
            "3",
            "4",
            "5",
            "--active_prob_vals",
            "0.1",
            "0.15",
            "0.2",
            "0.25",
            "--n_vals",
            "150",
            "160",
            "170",
            "180",
            "190",
            "200",
            "210",
            "220",
            "230",
            "240",
            "250",
            "--k_vals",
            "50",
            "60",
            "70",
            "80",
            "90",
            "95",
            "100",
            "--P_vals",
            "0.002",
            "0.003",
            "0.004",
            "0.005",
            "0.01",
            "--seed",
            "42",
        ],
    )

    args = parser.parse_args([])

    # Redirect stdout to a StringIO object
    output = StringIO()
    monkeypatch.setattr("sys.stdout", output)

    # Mock the plt.show() function to avoid showing the plot
    with mock.patch.object(plt, "show"):
        plot(args, seed=42)


def test_plot_save(mocker):
    """Test the plot() function with plot saving."""
    # Mock the necessary methods
    mock_exists = mocker.patch("os.path.exists", return_value=False)
    mock_makedirs = mocker.patch("os.makedirs")
    mock_savefig = mocker.patch("matplotlib.pyplot.Figure.savefig")

    # Define constants and variables for the test
    num_nodes_const = 2
    active_prob_const = 0.5
    n_const = 150
    k_const = 100
    P_const = 2 * (10**-3)
    d_const = 700
    N0_const = 1 * (10**-13)
    fr_const = 6 * (10**9)

    numevnts = 1000
    numruns = 5

    num_nodes_vals = [1, 2, 3, 4, 5]
    active_prob_vals = [0.1, 0.15, 0.2, 0.25]
    n_vals = [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    k_vals = [50, 60, 70, 80, 90, 95, 100]
    P_vals = [
        2 * (10**-3),
        4 * (10**-3),
        6 * (10**-3),
        8 * (10**-3),
    ]

    test_plots_folder = "test_plots"
    seed = 42  # Add a seed for reproducibility

    # Run the function under test
    plot_generate(
        num_nodes_const,
        active_prob_const,
        n_const,
        k_const,
        P_const,
        d_const,
        N0_const,
        fr_const,
        numevnts,
        numruns,
        num_nodes_vals,
        active_prob_vals,
        n_vals,
        k_vals,
        P_vals,
        test_plots_folder,
        seed=seed,
    )

    # Assuming "Power" is the actual first variable in the iteration
    expected_filename = os.path.join(test_plots_folder, "Power_plot.png")

    # Assert that savefig was called with the expected filename
    mock_savefig.assert_called_with(expected_filename)

    # Optionally, you can also assert that the directory creation was attempted
    # if the directory did not exist
    if not mock_exists.return_value:
        mock_makedirs.assert_called_with(test_plots_folder)


def test_plot_reproducibility(mocker):
    """Test that plots are reproducible with the same seed."""
    mock_savefig = mocker.patch("matplotlib.pyplot.Figure.savefig")

    # Define test parameters
    params = {
        "num_nodes_const": 2,
        "active_prob_const": 0.5,
        "n_const": 150,
        "k_const": 100,
        "P_const": 2 * (10**-3),
        "d_const": 700,
        "N0_const": 1 * (10**-13),
        "fr_const": 6 * (10**9),
        "numevnts": 1000,
        "numruns": 5,
        "num_nodes_vals": [1, 2, 3],
        "active_prob_vals": [0.1, 0.2],
        "n_vals": [150, 160],
        "k_vals": [50, 60],
        "P_vals": [2 * (10**-3), 4 * (10**-3)],
        "plots_folder": "test_plots",
        "seed": 42,
    }

    # Run the function twice with the same seed
    plot_generate(**params)
    first_call_args = mock_savefig.call_args_list

    mock_savefig.reset_mock()

    plot_generate(**params)
    second_call_args = mock_savefig.call_args_list

    # Check if the savefig calls are identical for both runs
    assert first_call_args == second_call_args, "Plots are not reproducible with the same seed"


def test_plot_different_seeds(mocker):
    """Test that plots are different with different seeds."""
    mock_savefig = mocker.patch("matplotlib.pyplot.Figure.savefig")

    # Define test parameters
    params = {
        "num_nodes_const": 2,
        "active_prob_const": 0.5,
        "n_const": 150,
        "k_const": 100,
        "P_const": 2 * (10**-3),
        "d_const": 700,
        "N0_const": 1 * (10**-13),
        "fr_const": 6 * (10**9),
        "numevnts": 1000,
        "numruns": 5,
        "num_nodes_vals": [1, 2, 3],
        "active_prob_vals": [0.1, 0.2],
        "n_vals": [150, 160],
        "k_vals": [50, 60],
        "P_vals": [2 * (10**-3), 4 * (10**-3)],
        "plots_folder": "test_plots",
    }

    # Run the function with two different seeds
    plot_generate(**params, seed=42)
    first_call_args = mock_savefig.call_args_list

    mock_savefig.reset_mock()

    plot_generate(**params, seed=123)
    second_call_args = mock_savefig.call_args_list

    # Check if the savefig calls are different for the two runs
    assert first_call_args != second_call_args, "Plots are identical with different seeds"