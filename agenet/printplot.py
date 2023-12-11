"""This module contains functions to print tables and plots."""
from __future__ import annotations

import argparse
import os
from typing import Any, cast

import matplotlib.pyplot as plt
from tabulate import tabulate

from agenet import run_main


def generate_table(
    num_nodes_const: int,
    active_prob_const: float,
    n_const: int,
    k_const: int,
    P_const: float,
    d_const: int,
    N0_const: float,
    fr_const: float,
    numevnts: int,
    numruns: int,
    num_nodes_vals: list[int],
    active_prob_vals: list[float],
    n_vals: list[int],
    k_vals: list[int],
    P_vals: list[float],
    file=None,
) -> None:
    """Print a table comparing the theoretical and simulated values.

    Args:
      num_nodes_const: Constant value for the number of nodes.
      active_prob_const: Constant value for the active probability.
      n_const: Constant value for the block length.
      k_const: Constant value for the update size.
      P_const: Constant value for the power.
      d_const: Constant value for the distance between nodes.
      N0_const: Constant value for the noise power.
      fr_const: Constant value for the frequency of the signal.
      numevnts: The number of events.
      numruns: The number of runs.
      num_nodes_vals: Values for the number of nodes.
      active_prob_vals: Values for the active probability.
      n_vals: Values for the block length.
      k_vals: Values for the update size.
      P_vals: Values for the power.
      file: File where to save table instead of printing it to standard output.
    """
    for i, var_name, var_vals in zip(
        range(5),
        [
            "number of nodes",
            "active probability",
            "block length",
            "update size",
            "Power",
        ],
        [
            num_nodes_vals,
            active_prob_vals,
            n_vals,
            k_vals,
            P_vals,
        ],
    ):
        const_vals: list[Any] = [
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
        ]

        headers = [var_name, "Theoretical", "Simulated"]

        table_rows = []
        for val in cast(list[int | float], var_vals):
            theoretical, simulated = run_main(
                *(const_vals[:i] + [val] + const_vals[i + 1 :])
            )
            table_rows.append([val, theoretical, simulated])

        if file is not None:
            file.write(tabulate(table_rows, headers=headers, tablefmt="grid") + "\n\n")
        else:
            print(tabulate(table_rows, headers=headers, tablefmt="grid"))
            print("\n")


def printage(args: argparse.Namespace) -> None:
    """Prints a table comparing results for different input values.

    Args:
      args: Parsed command-line arguments.
    """
    num_nodes_const = args.num_nodes_const
    active_prob_const = args.active_prob_const
    n_const = args.n_const
    k_const = args.k_const
    P_const = args.P_const
    d_const = args.d_const
    N0_const = args.N0_const
    fr_const = args.fr_const

    num_nodes_vals = args.num_nodes_vals
    active_prob_vals = args.active_prob_vals
    n_vals = args.n_vals
    k_vals = args.k_vals
    P_vals = args.P_vals

    generate_table(
        num_nodes_const=num_nodes_const,
        active_prob_const=active_prob_const,
        n_const=n_const,
        k_const=k_const,
        P_const=P_const,
        d_const=d_const,
        N0_const=N0_const,
        fr_const=fr_const,
        numevnts=args.numevnts,
        numruns=args.numruns,
        num_nodes_vals=num_nodes_vals,
        active_prob_vals=active_prob_vals,
        n_vals=n_vals,
        k_vals=k_vals,
        P_vals=P_vals,
    )


def plot_generate(
    num_nodes_const: int,
    active_prob_const: float,
    n_const: int,
    k_const: int,
    P_const: float,
    d_const: int,
    N0_const: float,
    fr_const: float,
    numevnts: int,
    numruns: int,
    num_nodes_vals: list[int],
    active_prob_vals: list[float],
    n_vals: list[int],
    k_vals: list[int],
    P_vals: list[float],
    plots_folder: str | None = None,
) -> None:
    """Plot the simulated and theoretical values for each variable.

    Args:
      num_nodes_const: Constant value for the number of nodes.
      active_prob_const: Constant value for the active probability.
      n_const: Constant value for the block length.
      k_const: Constant value for the update size.
      P_const: Constant value for the power.
      d_const: Constant value for the distance between nodes.
      N0_const: Constant value for the noise power.
      fr_const: Constant value for the frequency of the signal.
      numevnts: Number of events.
      numruns: Number of runs.
      num_nodes_vals: Values for the number of nodes.
      active_prob_vals: Values for the active probability.
      n_vals: Values for the block length.
      k_vals: Values for the update size.
      P_vals: Values for the power.
      plots_folder: Folder to save the plots.
    """
    for i, var_name, var_vals in zip(
        range(5),
        [
            "number of nodes",
            "active probability",
            "block length",
            "update size",
            "Power",
        ],
        [num_nodes_vals, active_prob_vals, n_vals, k_vals, P_vals],
    ):
        const_vals: list[Any] = [
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
        ]

        theoretical_vals = []
        simulated_vals = []

        # Gather data for each value of the variable
        for val in cast(list[int | float], var_vals):
            theoretical, simulated = run_main(
                *(const_vals[:i] + [val] + const_vals[i + 1 :])
            )
            theoretical_vals.append(theoretical)
            simulated_vals.append(simulated)

        # Create a new plot for each variable
        fig, ax = plt.subplots()
        ax.plot(var_vals, theoretical_vals, label="Theoretical", marker="o")
        ax.plot(var_vals, simulated_vals, label="Simulated", marker="x")
        ax.set_xlabel(var_name)
        ax.set_ylabel("Values")
        ax.set_title(f"Theoretical vs Simulated Values for Varying {var_name}")
        ax.legend()
        ax.grid(True)

        # Save each plot with a unique filename
        if plots_folder:
            if not os.path.exists(plots_folder):
                os.makedirs(plots_folder)
            fig.savefig(os.path.join(plots_folder, f"{var_name}_plot.png"))
            plt.close(fig)  # Close the plot after saving
        else:
            plt.show()


def plot(args: argparse.Namespace, plots_folder=None) -> None:
    """Plot the simulated and theoretical values for each variable and save the plots.

    Args:
        args: Parsed command-line arguments.
        plots_folder: Folder to save plots
    """
    # Extracting values from the args
    num_nodes_const = args.num_nodes_const
    active_prob_const = args.active_prob_const
    n_const = args.n_const
    k_const = args.k_const
    P_const = args.P_const
    d_const = args.d_const
    N0_const = args.N0_const
    fr_const = args.fr_const

    num_nodes_vals = args.num_nodes_vals
    active_prob_vals = args.active_prob_vals
    n_vals = args.n_vals
    k_vals = args.k_vals
    P_vals = args.P_vals

    # Call plot_generate to create and save plots
    plot_generate(
        num_nodes_const=num_nodes_const,
        active_prob_const=active_prob_const,
        n_const=n_const,
        k_const=k_const,
        P_const=P_const,
        d_const=d_const,
        N0_const=N0_const,
        fr_const=fr_const,
        numevnts=args.numevnts,
        numruns=args.numruns,
        num_nodes_vals=num_nodes_vals,
        active_prob_vals=active_prob_vals,
        n_vals=n_vals,
        k_vals=k_vals,
        P_vals=P_vals,
        plots_folder=plots_folder,
    )


def _parse_args() -> None:
    """Command-line arguments and calls the printage function."""
    parser = argparse.ArgumentParser(
        description="Prints a table comparing results for different input values."
    )
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
        "--d_const",
        type=int,
        default=700,
        help="Constant value for the distance between nodes.",
    )
    parser.add_argument(
        "--N0_const",
        type=float,
        default=1 * (10**-13),
        help="Constant value for the noise power.",
    )
    parser.add_argument(
        "--fr_const",
        type=float,
        default=6 * (10**9),
        help="Constant value for the frequency of the signal.",
    )
    parser.add_argument(
        "--numevnts", type=int, default=500, help="The number of events."
    )
    parser.add_argument("--numruns", type=int, default=100, help="The number of runs.")

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
            4 * (10**-3),
            6 * (10**-3),
            8 * (10**-3),
        ],
        help="Values for the power.",
    )
    parser.add_argument("--quiet", action="store_true", help="Omit tables")
    parser.add_argument("--plots", action="store_true", help="Show plots")
    parser.add_argument("--plots_folder", type=str, help="Folder to save plots")

    args = parser.parse_args()

    if not args.quiet:
        printage(args)

    if args.plots or args.plots_folder:
        plot(args, args.plots_folder if args.plots_folder else None)


if __name__ == "__main__":
    _parse_args()
