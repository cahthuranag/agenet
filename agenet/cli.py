"""Command-line interface for the agenet package."""

import argparse

from .bler import blercal_th
from .printplot import generate_table, plot
from .snratio import snr_th


def _main() -> None:
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
    parser.add_argument(
        "--blockerror", action="store_true", help="Show theoretical block error"
    )
    parser.add_argument("--snr", action="store_true", help="Show snr")
    parser.add_argument("--csv_location", type=str, help="Location to save csv file")

    args = parser.parse_args()

    output_action_taken = False

    if args.plots or args.plots_folder:
        plot(args, args.plots_folder if args.plots_folder else None)
        output_action_taken = True

    if args.snr:
        snr_th_val = snr_th(args.N0_const, args.d_const, args.P_const, args.fr_const)
        print(f"Theoretical SNR: {snr_th_val}")
        output_action_taken = True

    if args.blockerror:
        ber_th = blercal_th(args.snr, args.n_const, args.k_const)
        print(f"Theoretical Block Error Rate: {ber_th}")
        output_action_taken = True

    if not output_action_taken and not args.quiet:
        generate_table(
            args.num_nodes_const,
            args.active_prob_const,
            args.n_const,
            args.k_const,
            args.P_const,
            args.d_const,
            args.N0_const,
            args.fr_const,
            args.numevnts,
            args.numruns,
            args.num_nodes_vals,
            args.active_prob_vals,
            args.n_vals,
            args.k_vals,
            args.P_vals,
            args.csv_location if args.csv_location else None,
        )
