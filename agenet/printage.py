import argparse
from typing import List

from tabulate import tabulate

from agenet.maincom import run_main


def generate_comparison_table(
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
    file=None,
) -> None:
    """
    Generates a table comparing the theoretical and simulated values for the given input values.
    """
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
            ],
        )
    ):
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

        headers = [var_name, "Theoretical", "Simulated"]

        table_rows = []
        for val in var_vals:
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
    """
    Prints a table comparing results for different input values based on the command-line arguments.
    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    Returns:
        None
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

    generate_comparison_table(
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
        "--n_const", type=int, default=150, help="Constant value for the block length."
    )
    parser.add_argument(
        "--k_const", type=int, default=100, help="Constant value for the update size."
    )
    parser.add_argument(
        "--P_const",
        type=float,
        default=2 * (10**-3),
        help="Constant value for the power.",
    )

    parser.add_argument(
        "--numevnts", type=int, default=100, help="The number of events."
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
        default=[2 * (10**-3), 4 * (10**-3), 6 * (10**-3), 8 * (10**-3)],
        help="Values for the power.",
    )
    args = parser.parse_args()
    printage(args)


if __name__ == "__main__":
    main()
