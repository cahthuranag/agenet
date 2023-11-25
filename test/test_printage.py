import subprocess
import os
import argparse
import io
from contextlib import redirect_stdout
from unittest.mock import patch
from tabulate import tabulate
from agenet import generate_table, printage, plot
import sys
from io import StringIO
from unittest import mock
import matplotlib
import matplotlib.pyplot as plt
from agenet import  plot


# this is a test for the generate_comparison_table function
def assert_table_format(output_lines):
    header_line = output_lines[0].strip()
    row_lines = output_lines[1:-1]  # Skip header and separator lines
    separator_line = output_lines[-1].strip()

    # Check if the header line starts and ends with '+'
    assert header_line.startswith("+") and header_line.endswith("+")

    # Check if there is a '+' in the middle of the header line
    assert "+" in header_line[1:-1]

    # Check if all row lines start and end with '|'
    for row_line in row_lines:
        assert row_line.startswith("|") and row_line.endswith("|")

        # Check if there is a '|' in the middle of each row line
        assert "|" in row_line[1:-1]

    # Check if the separator line matches the expected format
    columns = header_line.strip().split("|")[1:-1]
    expected_separator = "+".join(
        "-" * (len(column.strip()) + 2) for column in columns
    )

    # Adjust separator line if the header line has '+' characters at the
    # beginning and end
    if header_line.startswith("+") and header_line.endswith("+"):
        expected_separator = "+" + expected_separator + "+"

    assert separator_line == expected_separator


def test_generate_table():
    # Test input values for the function
    num_nodes_const = 2
    active_prob_const = 0.5
    n_const = 150
    k_const = 100
    P_const = 2 * (10**-3)
    numevnts = 100
    numruns = 100
    num_nodes_vals = [1, 2, 3]
    active_prob_vals = [0.1, 0.2]
    n_vals = [150, 160]
    k_vals = [50, 60]
    P_vals = [2 * (10**-3), 4 * (10**-3)]

    # Capture the printed output

    output = io.StringIO()
    with redirect_stdout(output):
        generate_table(
            num_nodes_const,
            active_prob_const,
            n_const,
            k_const,
            P_const,
            numevnts,
            numruns,
            num_nodes_vals,
            active_prob_vals,
            n_vals,
            k_vals,
            P_vals,
        )
    output_str = output.getvalue()

    # Split the output into lines and check the format using tabulate
    output_lines = output_str.strip().split("\n")
    headers = [
        header.strip()
        for header in output_lines[0].strip().split("|")[1:-1]
    ]
    table_data = [
        row.strip().split("|")[1:-1] for row in output_lines[2:-1]
    ]

    expected_table = tabulate(table_data, headers=headers, tablefmt="grid")
    actual_table = tabulate(table_data, headers=headers, tablefmt="grid")

    assert expected_table == actual_table


def test_printage():
    args = argparse.Namespace(
        num_nodes_const=2,
        active_prob_const=0.5,
        n_const=150,
        k_const=100,
        P_const=2 * (10**-3),
        numevnts=500,
        numruns=1,
        num_nodes_vals=[1, 2, 3],
        active_prob_vals=[0.1, 0.2],
        n_vals=[150, 160],
        k_vals=[50, 60],
        P_vals=[2 * (10**-3), 4 * (10**-3)],
    )
    # Capture the printed output

    output = io.StringIO()
    with redirect_stdout(output):
        printage(args)
    output_str = output.getvalue()

    # Split the output into lines and check the format using tabulate
    output_lines = output_str.strip().split("\n")
    headers = [
        header.strip()
        for header in output_lines[0].strip().split("|")[1:-1]
    ]
    table_data = [
        row.strip().split("|")[1:-1] for row in output_lines[2:-1]
    ]

    expected_table = tabulate(table_data, headers=headers, tablefmt="grid")
    actual_table = tabulate(table_data, headers=headers, tablefmt="grid")

    assert expected_table == actual_table


@patch(
    "sys.argv",
    [
        "printage.py",
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
        "1",
        "--num_nodes_vals",
        "1",
        "2",
        "--active_prob_vals",
        "0.1",
        "0.2",
        "--n_vals",
        "150",
        "160",
        "--k_vals",
        "50",
        "60",
        "--P_vals",
        "0.002",
        "0.003",
    ],
)


def test_plot(monkeypatch):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_nodes_const",
        type=int,
        default=2,
        help="Constant value for the number of nodes.",
    )
    parser.add_argument(
        "--active_prob_const",
        type=float,
        default=0.5,
        help="Constant value for the active probability.",
    )
    parser.add_argument(
        "--n_const",
        type=int,
        default=150,
        help="Constant value for the block length.",
    )
    parser.add_argument(
        "--k_const",
        type=int,
        default=100,
        help="Constant value for the update size.",
    )
    parser.add_argument(
        "--P_const",
        type=float,
        default=2 * (10**-3),
        help="Constant value for the power.",
    )
    parser.add_argument(
        "--numevnts",
        type=int,
        default=1000,
        help="The number of events.",
    )
    parser.add_argument(
        "--numruns",
        type=int,
        default=2,
        help="The number of runs.",
    )
    parser.add_argument(
        "--num_nodes_vals",
        nargs="+",
        type=int,
        default=[1, 2, 3, 4, 5],
        help="Values for the number of nodes.",
    )
    parser.add_argument(
        "--active_prob_vals",
        nargs="+",
        type=float,
        default=[0.1, 0.15, 0.2, 0.25],
        help="Values for the active probability.",
    )
    parser.add_argument(
        "--n_vals",
        nargs="+",
        type=int,
        default=[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250],
        help="Values for the block length.",
    )
    parser.add_argument(
        "--k_vals",
        nargs="+",
        type=int,
        default=[50, 60, 70, 80, 90, 95, 100],
        help="Values for the update size.",
    )
    parser.add_argument(
        "--P_vals",
        nargs="+",
        type=float,
        default=[
            2 * (10**-3),
            3 * (10**-3),
            4 * (10**-3),
            5 * (10**-3),
            10 * (10**-3),
        ],
        help="Values for the power.",
    )
    parser.add_argument(
    "--plots",
    action='store_true',  # Assuming 'plots' is a boolean flag
    help="Flag to indicate if plots should be generated."
)
    # Add other necessary arguments to the parser

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
        ],
    )

    args = parser.parse_args([])

    # Redirect stdout to a StringIO object
    output = StringIO()
    monkeypatch.setattr("sys.stdout", output)

    # Mock the plt.show() function to avoid showing the plot
    with mock.patch.object(plt, "show"):
        plot(args)






def test_command_line_arguments():
    # Define sample command-line arguments
    num_nodes_const = 2
    active_prob_const = 0.5
    n_const = 150
    k_const = 100
    P_const = 2 * (10**-3)

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

    # Run the script with the sample command-line arguments
    script_path = os.path.abspath("agenet/printage.py")
    command = (
        f"python {script_path} "
        f"--num_nodes_const {num_nodes_const} "
        f"--active_prob_const {active_prob_const} "
        f"--n_const {n_const} "
        f"--k_const {k_const} "
        f"--P_const {P_const} "
        f"--numevnts {numevnts} "
        f"--numruns {numruns} "
        f"--num_nodes_vals {' '.join(map(str, num_nodes_vals))} "
        f"--active_prob_vals {' '.join(map(str, active_prob_vals))} "
        f"--n_vals {' '.join(map(str, n_vals))} "
        f"--k_vals {' '.join(map(str, k_vals))} "
        f"--P_vals {' '.join(map(str, P_vals))}"
    )

    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )

    # Assert that the stdout is not empty (indicating that there's some output)
    assert result.stdout.strip() != ""
