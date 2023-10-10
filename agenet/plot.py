# Copyright (c) 2023 Chathuranga M. Basnayaka and Nuno Fachada
# Distributed under the MIT License. See LICENSE.md for more info.
import argparse
from typing import List

import matplotlib.pyplot as plt

from agenet.maincom import run_main


def plot_generate(
    num_nodes_const: int,
    active_prob_const: float,
    n_const: int,
    k_const: int,
    P_const: float,
    numevnts: int,
    numruns: int,
    num_nodes_vals: List[int],
    active_prob_vals: List[float],
    n_vals: List[int],
    k_vals: List[int],
    P_vals: List[float],
) -> plt.Figure:
    """
    Plot the simulated and theoretical for each variable.

    Args:
        numevnts (int, optional): The number of events. Default is 1000.
        numruns (int, optional): The number of runs. Default is 100.

    Returns:
        plt.Figure: The generated figure.
    """

    # initialize the minimum and maximum values for the x and y-axes
    x_min, x_max = float("inf"), float("-inf")
    y_min, y_max = float("inf"), float("-inf")

    for i, (var_name, var_vals) in enumerate(
        zip(
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
                numevnts,
                numruns,
            ],
        )
    ):
        # create a list of the constant values with the loop variable set to None
        const_vals = [
            num_nodes_const,
            active_prob_const,
            n_const,
            k_const,
            P_const,
            numevnts,
            numruns,
        ]
        const_vals[i] = None

        # create a new figure and plot the simulated and theoretical values
        # with the constant values
        fig, ax = plt.subplots()
        ax.plot(
            var_vals,
            [
                run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))[
                    0
                ]
                for val in var_vals
            ],
            label="Theoretical",
        )
        ax.plot(
            var_vals,
            [
                run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))[
                    1
                ]
                for val in var_vals
            ],
            label="Simulated",
        )
        ax.set_xlabel(var_name)
        ax.legend()
        ax.set_title(
            f"Plot of Simulated and Theoretical Values respect to {var_name}"
        )

        # update the minimum and maximum values for the x and y-axes
        x_min = min(x_min, min(var_vals))
        x_max = max(x_max, max(var_vals))
        y_min = min(
            y_min,
            min(
                min(
                    [
                        run_main(
                            *(const_vals[:i] + [val] + const_vals[i + 1 :])
                        )
                        for val in var_vals
                    ]
                )
            ),
        )
        y_max = max(
            y_max,
            max(
                max(
                    [
                        run_main(
                            *(const_vals[:i] + [val] + const_vals[i + 1 :])
                        )
                        for val in var_vals
                    ]
                )
            ),
        )

    # set the x and y-axis limits based on the updated minimum and maximum values
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)


def plot(args: argparse.Namespace) -> None:
    import matplotlib.pyplot as plt

    """
    Plot the simulated and theoretical for each variable.
    Args:
        args (argparse.Namespace): Parsed command-line arguments.
        Num_nodes_const (int, optional): The number of nodes. Default is 2.
        active_prob_const (float, optional): The active probability. 
        n_const (int, optional): The block length. 
        k_const (int, optional): The update size.
        P_const (float, optional): The power. 
        numevnts (int, optional): The number of events. 
        numruns (int, optional): The number of runs.
        num_nodes_vals (List[int], optional): The list of number of nodes.
        active_prob_vals (List[float], optional): The list of active probability.
        n_vals (List[int], optional): The list of block length.
        k_vals (List[int], optional): The list of update size.
        P_vals (List[float], optional): The list of power.
    Returns:
     plt.Figure: The generated figure.
    """
    num_nodes_const = args.num_nodes_const
    active_prob_const = args.active_prob_const
    n_const = args.n_const
    k_const = args.k_const
    P_const = args.P_const

    num_nodes_vals = args.num_nodes_vals
    active_prob_vals = args.active_prob_vals
    n_vals = args.n_vals
    k_vals = args.k_vals
    P_vals = args.P_vals

    plot_generate(
        num_nodes_const=num_nodes_const,
        active_prob_const=active_prob_const,
        n_const=n_const,
        k_const=k_const,
        P_const=P_const,
        numevnts=args.numevnts,
        numruns=args.numruns,
        num_nodes_vals=num_nodes_vals,
        active_prob_vals=active_prob_vals,
        n_vals=n_vals,
        k_vals=k_vals,
        P_vals=P_vals,
    )
    plt.show()


def main() -> None:
    """
    Main function that parses the command-line arguments and calls the printage function.
    Returns:
        None
    """
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
        "--numevnts", type=int, default=1000, help="The number of events."
    )
    parser.add_argument(
        "--numruns", type=int, default=100, help="The number of runs."
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
    args = parser.parse_args()
    plot(args)


if __name__ == "__main__":
    main()
