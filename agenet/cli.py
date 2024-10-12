"""Command-line interface for AgeNet."""

from __future__ import annotations

import argparse
import importlib.metadata
import sys

import matplotlib.pyplot as plt

from .blkerr import block_error_th
from .simulation import multi_param_ev_sim
from .snratio import snr_th


def _main():

    def_params = {
        "distance": [100],
        "N0": [1e-13],
        "frequency": [6e6],
        "num-events": [50],
        "num-nodes": [5],
        "active-prob": [0.2],
        "num-bits": [150],
        "info-bits": [50],
        "power": [7e-2, 8e-2, 9e-2],
    }

    def_params_str = {
        key: " ".join(map(str, value)) for key, value in def_params.items()
    }

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
        default=def_params["distance"],
        help=f"Distance between nodes in meters (default: {def_params_str['distance']})",
    )
    parser.add_argument(
        "-N",
        "--N0",
        type=float,
        nargs="+",
        default=def_params["N0"],
        help=f"Noise power in Watts (default: {def_params_str['N0']})",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        type=float,
        nargs="+",
        default=def_params["frequency"],
        help=f"Signal frequency in Hz (default: {def_params_str['frequency']})",
    )
    parser.add_argument(
        "-e",
        "--num-events",
        type=int,
        nargs="+",
        default=def_params["num-events"],
        help=f"Number of events (default: {def_params_str['num-events']})",
    )
    parser.add_argument(
        "-m",
        "--num-nodes",
        type=int,
        nargs="+",
        default=def_params["num-nodes"],
        help=f"Number of nodes (default: {def_params_str['num-nodes']})",
    )
    parser.add_argument(
        "-a",
        "--active-prob",
        type=float,
        nargs="+",
        default=def_params["active-prob"],
        help=f"Active probability (default: {def_params_str['active-prob']})",
    )
    parser.add_argument(
        "-n",
        "--num-bits",
        type=int,
        nargs="+",
        default=def_params["num-bits"],
        help=f"Total number of bits (default: {def_params_str['num-bits']})",
    )
    parser.add_argument(
        "-k",
        "--info-bits",
        type=int,
        nargs="+",
        default=def_params["info-bits"],
        help=f"Number of information bits (default: {def_params_str['info-bits']})",
    )
    parser.add_argument(
        "-P",
        "--power",
        type=float,
        nargs="+",
        default=def_params["power"],
        help=f"Transmission power in Watts (default: {def_params_str['power']})",
    )
    parser.add_argument(
        "-r",
        "--num-runs",
        type=int,
        default=10,
        help="Number of simulation runs (default: %(default)s)",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Seed for random number generator (a random seed will be used by default)",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output")
    parser.add_argument(
        "-p",
        "--plot-show",
        action="store_true",
        help="Show plot (only valid if exactly one parameter varies)",
    )
    parser.add_argument(
        "--plot-save",
        type=str,
        default="",
        metavar="IMAGE_FILE",
        help="Save plot to file (only valid if exactly one parameter varies, extension determines file type)",
    )

    parser.add_argument(
        "--csv", type=str, help="Save results to CSV file", metavar="CSV_FILE"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + importlib.metadata.version("agenet"),
    )

    args = parser.parse_args()

    # Run the simulations
    results = multi_param_ev_sim(
        distance=args.distance,
        N0=args.N0,
        frequency=args.frequency,
        num_events=args.num_events,
        num_nodes=args.num_nodes,
        active_prob=args.active_prob,
        num_bits=args.num_bits,
        info_bits=args.info_bits,
        power=args.power,
        num_runs=args.num_runs,
        seed=args.seed,
    )

    # Process output options
    if not args.quiet:

        theoretical_snr = snr_th(
            args.N0[0], args.distance[0], args.power[0], args.frequency[0]
        )
        print(f"Theoretical SNR: {theoretical_snr}")

        theoretical_bler = block_error_th(
            args.num_bits[0], args.info_bits[0], args.power[0]
        )
        print(f"Theoretical Block Error Rate: {theoretical_bler}")

        print(results)

    if args.csv:
        results.to_csv(args.csv, index=False)
        print(f"Simulation results saved to {args.csv}")

    if args.plot_show or len(args.plot_save) > 0:
        aoi_vs_param: tuple[str, str, list[float | int]]
        num_var_params = 0
        for param_info in [
            ("distance", "Distance (m)", args.distance),
            ("N0", "N0 - Noise power (W)", args.N0),
            ("frequency", "Frequency (Hz)", args.frequency),
            ("num_events", "Number of events", args.num_events),
            ("num_nodes", "Number of nodes", args.num_nodes),
            ("active_prob", "Active probability", args.active_prob),
            ("num_bits", "n - Number of bits", args.num_bits),
            ("info_bits", "k - Information bits", args.info_bits),
            ("power", "P - Transmission power (W)", args.power),
        ]:

            if len(param_info[2]) > 1:
                num_var_params += 1
                aoi_vs_param = param_info

        if num_var_params == 1:
            results_sorted = results.sort_values(aoi_vs_param[0])

            fig, ax = plt.subplots()
            aaoi_theory = results_sorted["aaoi_theory"]
            aaoi_sim = results_sorted["aaoi_sim"]
            ax.plot(results_sorted[aoi_vs_param[0]], aaoi_theory, label="Theoretical")
            ax.plot(results_sorted[aoi_vs_param[0]], aaoi_sim, label="Simulation")
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
