"""This module contains functions to print tables and plots."""
from __future__ import annotations

import argparse
import os
from typing import List, Union, cast, Any

import matplotlib.pyplot as plt
from tabulate import tabulate

from .maincom import run_simulation

import csv


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
    csv_location: str = None,
) -> None:
    """Print a table comparing the theoretical and simulated values.

    Args:
        num_nodes_const, active_prob_const, n_const, k_const, P_const, d_const, N0_const, fr_const: Constant simulation parameters.
        numevnts: The number of events.
        numruns: The number of runs.
        num_nodes_vals, active_prob_vals, n_vals, k_vals, P_vals: Lists of parameter values to simulate.
        csv_location: Optional; path to save the table to a CSV file.
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
        for val in cast(List[Union[int, float]], var_vals):
            theoretical, simulated = run_simulation(
                *(const_vals[:i] + [val] + const_vals[i + 1 :])
            )
            table_rows.append([val, theoretical, simulated])
        
        if csv_location is not None:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(csv_location), exist_ok=True)
            
            with open(csv_location, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(table_rows)
        else:
            # If no CSV location is provided, or to additionally print the result:
            from tabulate import tabulate  # You might need to install this package
            print(tabulate(table_rows, headers=headers, tablefmt="grid"))
            print("\n")

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
        for val in cast(List[Union[int, float]], var_vals):
            theoretical, simulated = run_simulation(
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


def plot(args: argparse.Namespace, plots_folder: str | None = None) -> None:
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
