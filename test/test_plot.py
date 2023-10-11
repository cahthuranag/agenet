import argparse
import os
import subprocess
import sys
from io import StringIO
from unittest import mock

import matplotlib
import matplotlib.pyplot as plt

from agenet.plot import main, plot


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


def test_main():
    matplotlib.use("Agg")
    sys.argv = [
        "agenet/plot.py",
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
    ]
    with mock.patch.object(plt, "show"):
        main()
        fig = plt.gcf()
        assert fig.get_figheight() > 0


def test_command_line_arguments():
    matplotlib.use("Agg")
    script_path = os.path.abspath("agenet/plot.py")

    # Run the script with the sample command-line arguments
    with mock.patch.object(plt, "show"):
        command = f"python {script_path} --numruns 1"
        process = subprocess.Popen(command, shell=True, text=True)
        fig = plt.gcf()
        assert fig.get_figheight() > 0
        plt.close("all")
        process.pid
