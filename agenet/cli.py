import argparse
import importlib.metadata
import sys

import matplotlib.pyplot as plt

from .blkerr import block_error_th
from .simulation import multi_param_ev_sim
from .snratio import snr_th


def _main():
    # Create a parser to parse our command line arguments
    parser = argparse.ArgumentParser(
        prog="agenet", description="Command line interface to AgeNet"
    )

    # Define our command line arguments
    parser.add_argument(
        "-d",
        "--distance",
        type=float,
        nargs="+",
        default=[100],
        help="Distance(s) in meters",
    )
    parser.add_argument(
        "-N",
        "--N0",
        type=float,
        nargs="+",
        default=[1e-13],
        help="Noise power(s) in Watts",
    )
    parser.add_argument(
        "-f",
        "--frame-rate",
        type=float,
        nargs="+",
        default=[6e6],
        help="Frame rate(s) in Hz",
    )
    parser.add_argument(
        "-e", "--num-events", type=int, nargs="+", default=[50], help="Number of events"
    )
    parser.add_argument(
        "-m", "--num-nodes", type=int, nargs="+", default=[5], help="Number of nodes"
    )
    parser.add_argument(
        "-a",
        "--active-prob",
        type=float,
        nargs="+",
        default=[0.2],
        help="Active probability",
    )
    parser.add_argument(
        "-n",
        "--number-of-bits",
        type=int,
        nargs="+",
        default=[150],
        help="Total number of bits",
    )
    parser.add_argument(
        "-k",
        "--info-bits",
        type=int,
        nargs="+",
        default=[50],
        help="Number of information bits",
    )
    parser.add_argument(
        "-P",
        "--dep-prob",
        type=float,
        nargs="+",
        default=[8e-2],
        help="Depolarizing probability",
    )
    parser.add_argument(
        "-r", "--num-runs", type=int, default=10, help="Number of simulation runs"
    )
    parser.add_argument("-s", "--seed", type=int, help="Random seed")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")
    parser.add_argument(
        "-p",
        "--plot-show",
        action="store_true",
        help="Plot results (only valid if exactly one parameter varies)",
    )
    parser.add_argument(
        "--plot-save",
        type=str,
        default="",
        help="Save plot to file (only valid if exactly one parameter varies)",
    )
    parser.add_argument(
        "--block-error",
        action="store_true",
        help="Calculate theoretical block error rate",
    )
    parser.add_argument("--snr", action="store_true", help="Calculate theoretical SNR")
    parser.add_argument("--csv", type=str, help="Save results to CSV file")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + importlib.metadata.version("agenet"),
    )

    args = parser.parse_args()

    # Always run the simulation
    result = multi_param_ev_sim(
        d=args.distance,
        N0=args.N0,
        fr=args.frame_rate,
        numevnts=args.num_events,
        num_nodes=args.num_nodes,
        active_prob=args.active_prob,
        n=args.number_of_bits,
        k=args.info_bits,
        P=args.dep_prob,
        numruns=args.num_runs,
        seed=args.seed,
    )

    # Process output options
    if not args.quiet:
        print(result)

    if args.snr:
        theoretical_snr = snr_th(args.N0[0], args.d[0], args.P[0], args.fr[0])
        if not args.quiet:
            print(f"Theoretical SNR: {theoretical_snr}")

    if args.block_error:
        theoretical_bler = block_error_th(args.n[0], args.k[0], args.P[0])
        if not args.quiet:
            print(f"Theoretical Block Error Rate: {theoretical_bler}")

    if args.csv:
        result.to_csv(args.csv, index=False)
        print(f"Simulation results saved to {args.csv}")

    if args.plot_show or len(args.plot_save) > 0:
        aoi_vs_param: tuple[str, list[float | int]]
        num_var_params = 0
        for param_info in [
            ("d", "Distance (m)", args.distance),
            ("N0", "N0 - Noise power (W)", args.N0),
            ("fr", "Frame rate (Hz)", args.frame_rate),
            ("numevnts", "Number of events", args.num_events),
            ("num_nodes", "Number of nodes", args.num_nodes),
            ("active_prob", "Active probability", args.active_prob),
            ("n", "n - Number of bits", args.number_of_bits),
            ("k", "k - Information bits", args.info_bits),
            ("P", "P - Depolarizing probability", args.dep_prob),
        ]:

            if len(param_info[2]) > 1:
                num_var_params += 1
                aoi_vs_param = param_info

        if num_var_params == 1:
            result_sorted = result.sort_values(aoi_vs_param[0])

            fig, ax = plt.subplots()
            aaoi_theory = result_sorted["av_age_theoretical"]
            aaoi_sim = result_sorted["av_age_simulation"]
            ax.plot(result_sorted[aoi_vs_param[0]], aaoi_theory, label="Theoretical")
            ax.plot(result_sorted[aoi_vs_param[0]], aaoi_sim, label="Simulation")
            ax.set_xlabel(aoi_vs_param[1])
            ax.set_ylabel("AAoI")
            ax.set_ylim([0, max(aaoi_theory.max(), aaoi_sim.max()) * 1.05])
            ax.legend()
            if len(args.plot_save) > 0:
                fig.savefig(args.plot_save)
            if args.plot_show:
                plt.show()
        else:
            print(
                f"Unable to create plot: only one variable parameter is allowed, but there are {num_var_params}.",
                file=sys.stderr,
            )
