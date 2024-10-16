"""Command-line interface for AgeNet."""

from __future__ import annotations

import argparse
import importlib.metadata
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value
from threading import Event
from time import sleep

import matplotlib.pyplot as plt
from rich import box
from rich.console import Console
from rich.progress import Progress
from rich_tools import df_to_table

from .simulation import multi_param_ev_sim


def _main():

    # Default arguments
    def_params = {
        "distance": [500],
        "N0": [1e-13],
        "frequency": [5e9],
        "num-events": [100],
        "num-bits": [400],
        "info-bits": [350],
        "power": [5e-3],
    }

    def_params_str = {
        key: " ".join(map(str, value)) for key, value in def_params.items()
    }

    # Create a parser to parse our command line arguments
    parser = argparse.ArgumentParser(
        prog="agenet", description="Command line interface to AgeNet"
    )

    # Simulation arguments
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

    # Number of monte carlo runs
    parser.add_argument(
        "-r",
        "--num-runs",
        type=int,
        default=10,
        help="Number of simulation runs (default: %(default)s)",
    )

    # Seed for reproducible runs
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Seed for random number generator (a random seed will be used by default)",
    )

    # Output specification parameters
    parser.add_argument(
        "-t", "--show-table", action="store_true", help="Show table with results"
    )

    parser.add_argument(
        "-o",
        "--save-csv",
        type=str,
        help="Save results to CSV file",
        metavar="CSV_FILE",
    )

    parser.add_argument(
        "-p",
        "--show-plot",
        action="store_true",
        help="Show plot (only valid if exactly one parameter varies)",
    )
    parser.add_argument(
        "--save-plot",
        type=str,
        default="",
        metavar="IMAGE_FILE",
        help="Save plot to file (only valid if exactly one parameter varies, extension determines file type)",
    )

    parser.add_argument(
        "--debug",
        choices=["0", "1", "2"],
        default="0",
        help="Level of debugging report if an error occurs (default: %(default)s)",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + importlib.metadata.version("agenet"),
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Create a rich console
    console = Console()

    # Determine the total number of steps (parameter combinations)
    total_steps = (
        len(args.distance)
        * len(args.N0)
        * len(args.frequency)
        * len(args.num_events)
        * len(args.num_bits)
        * len(args.info_bits)
        * len(args.power)
    )

    # Create a shared counter for keeping tabs on the simulation progress
    # Type 'i' means signed integer
    counter = Value("i", 0)

    # Event for signalling the simulation to stop
    stop_event = Event()

    # Run the simulation within the context of a progress bar
    with Progress() as progress:
        task = progress.add_task("[white]Simulating...", total=total_steps)

        with ThreadPoolExecutor(max_workers=1) as executor:

            # Execute the simulation in a separate thread
            future = executor.submit(
                multi_param_ev_sim,
                frequency=args.frequency,
                num_events=args.num_events,
                distance=args.distance,
                N0=args.N0,
                num_bits=args.num_bits,
                info_bits=args.info_bits,
                power=args.power,
                num_runs=args.num_runs,
                seed=args.seed,
                counter=counter,
                stop_event=stop_event,
            )

            try:
                # Update progress bar while the simulation is running
                while not future.done():
                    # Small delay to avoid excessive CPU usage
                    sleep(0.1)
                    # Update progress bar a little bit more
                    progress.update(task, completed=counter.value)

            except KeyboardInterrupt:
                stop_event.set()
                progress.stop()
                err_console = Console(stderr=True)
                err_console.print("[dark_orange bold]Simulation terminated by user!")

            # Get the result after the task finishes
            results = future.result()

    try:
        # Process output options
        if args.show_table:

            table = df_to_table(results)
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            console.print(table)

        if args.save_csv:
            results.to_csv(args.save_csv, index=False)
            console.print(f"Simulation results saved to {args.save_csv}")

        if args.show_plot or len(args.save_plot) > 0:
            aoi_vs_param: tuple[str, str, list[float | int]]
            num_var_params = 0
            for param_info in [
                ("distance", "Distance (m)", args.distance),
                ("N0", "N0 - Noise power (W)", args.N0),
                ("frequency", "Frequency (Hz)", args.frequency),
                ("num_events", "Number of events", args.num_events),
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
                ax.plot(
                    results_sorted[aoi_vs_param[0]], aaoi_theory, label="Theoretical"
                )
                ax.plot(results_sorted[aoi_vs_param[0]], aaoi_sim, label="Simulation")
                ax.set_xlabel(aoi_vs_param[1])
                ax.set_ylabel("AAoI")
                ax.set_ylim([0, max(aaoi_theory.max(), aaoi_sim.max()) * 1.05])
                ax.legend()
                if len(args.save_plot) > 0:
                    fig.savefig(args.save_plot)
                if args.show_plot:
                    plt.show()
            else:
                raise ValueError(
                    f"Unable to create plot: only one variable parameter is allowed, but there are {num_var_params}."
                )

    except Exception as e:
        stop_event.set()
        err_console = Console(stderr=True)
        if args.debug == "0":
            err_console.print(e)
        elif args.debug == "1":
            err_console.print_exception()
        else:
            err_console.print_exception(show_locals=True)
