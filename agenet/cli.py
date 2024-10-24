"""Command-line interface for AgeNet."""

from __future__ import annotations

import argparse
import importlib.metadata
import sys
from collections.abc import MutableSequence
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from multiprocessing import Value
from threading import Event
from time import sleep
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
from rich import box
from rich.console import Console
from rich.progress import Progress, SpinnerColumn
from rich.style import Style
from rich_argparse import RichHelpFormatter
from rich_tools import df_to_table

from .simulation import multi_param_ev_sim


def _main() -> int:
    """Function invoked when running the agenet command at the terminal."""
    # Configure Rich consoles for enhanced terminal output
    err_console = Console(stderr=True, highlight=False)
    console = Console(highlight=False)

    class MsgType(Enum):
        """Different types of summary item."""

        INFO = (1, Style(color="green"), console)
        WARNING = (2, Style(color="dark_goldenrod"), console)
        ERROR = (3, Style(color="bright_red"), err_console)

        # Custom initializer to unpack the tuple
        def __init__(self, code, style, console):
            self.code = code
            self.style = style
            self.console = console

    class RunLogMsg(NamedTuple):
        """Class for log messages."""

        message: str
        """Log message."""

        msg_type: MsgType
        """Type of message."""

    # Package version
    agenet_version = importlib.metadata.version("agenet")

    # Color of the "agenet" word / command
    agenet_color = "grey42"
    RichHelpFormatter.styles["argparse.prog"] = agenet_color

    # Run log
    run_log: MutableSequence[RunLogMsg] = []

    # Possible plot to display
    plot_to_display = None

    # Return code, by default 0, meaning no errors
    return_code = 0

    # Default arguments
    def_params: dict[str, list[float]] = {
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
        prog="agenet",
        description="Agenet is a Python package to estimate the Age of Information in cooperative wireless networks",
        formatter_class=lambda prog: RichHelpFormatter(prog, console=console),
    )

    # Custom error formatting function for ArgumentParser
    def custom_args_error(self, message):
        self.print_usage()
        err_console.print(message, style=MsgType.ERROR.style)
        sys.exit(2)

    # Monkey patch the ArgumentParser class to replace its error method
    setattr(argparse.ArgumentParser, "error", custom_args_error)

    # Global simulation parameters
    general_group = parser.add_argument_group(
        "General", "General simulation parameters"
    )

    general_group.add_argument(
        "-f",
        "--frequency",
        type=float,
        nargs="+",
        default=def_params["frequency"],
        help=f"Signal frequency in Hz (default: {def_params_str['frequency']})",
    )

    general_group.add_argument(
        "-e",
        "--num-events",
        type=int,
        nargs="+",
        default=def_params["num-events"],
        help=f"Number of events in a simulation run (default: {def_params_str['num-events']})",
    )

    general_group.add_argument(
        "-r",
        "--num-runs",
        type=int,
        default=10,
        help="Number of simulation runs (default: %(default)s)",
    )

    general_group.add_argument(
        "-s",
        "--seed",
        type=int,
        help="Seed for random number generator (a random seed will be used by default)",
    )

    # Per node simulation parameters
    node1_group = parser.add_argument_group(
        "Node", "Node (or source node) simulation parameters"
    )

    node1_group.add_argument(
        "--num-bits",
        type=int,
        nargs="+",
        default=def_params["num-bits"],
        help=f"Total number of bits (default: {def_params_str['num-bits']})",
    )
    node1_group.add_argument(
        "--info-bits",
        type=int,
        nargs="+",
        default=def_params["info-bits"],
        help=f"Number of information bits (default: {def_params_str['info-bits']})",
    )
    node1_group.add_argument(
        "--power",
        type=float,
        nargs="+",
        default=def_params["power"],
        help=f"Transmission power in Watts (default: {def_params_str['power']})",
    )
    node1_group.add_argument(
        "--distance",
        type=float,
        nargs="+",
        default=def_params["distance"],
        help=f"Distance between nodes in meters (default: {def_params_str['distance']})",
    )
    node1_group.add_argument(
        "--N0",
        type=float,
        nargs="+",
        default=def_params["N0"],
        help=f"Noise power in Watts (default: {def_params_str['N0']})",
    )

    # Relay-specific simulation parameters
    node2_group = parser.add_argument_group(
        "Relay",
        "Relay-specific simulation parameters (if different than source node)",
    )

    node2_group.add_argument(
        "--num-bits-2",
        type=int,
        nargs="*",
        default=[None],
        help="Total number of bits in relay (defaults to --num-bits)",
    )
    node2_group.add_argument(
        "--info-bits-2",
        type=int,
        nargs="*",
        default=[None],
        help="Number of information bits in relay (defaults to --info-bits)",
    )
    node2_group.add_argument(
        "--power-2",
        type=float,
        nargs="*",
        default=[None],
        help="Transmission power in Watts in relay (defaults to --power)",
    )
    node2_group.add_argument(
        "--distance-2",
        type=float,
        nargs="*",
        default=[None],
        help="Distance between relay and destination (defaults to --distance)",
    )
    node2_group.add_argument(
        "--N0-2",
        type=float,
        nargs="*",
        default=[None],
        help="Noise power in Watts in relay (defaults to --N0)",
    )

    # Output specification parameters
    output_group = parser.add_argument_group(
        "Output", "Output specification parameters"
    )

    output_group.add_argument(
        "-t", "--show-table", action="store_true", help="Show table with results"
    )

    output_group.add_argument(
        "-o",
        "--save-csv",
        type=str,
        help="Save results to CSV file",
        metavar="CSV_FILE",
    )

    output_group.add_argument(
        "-p",
        "--show-plot",
        action="store_true",
        help="Show plot (only valid if exactly one parameter varies)",
    )
    output_group.add_argument(
        "--save-plot",
        metavar="IMAGE_FILE",
        help="Save plot to file (only valid if exactly one parameter varies, extension determines file type)",
    )

    output_group.add_argument(
        "--debug",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Level of debugging report if an error occurs (default: %(default)s)",
    )

    output_group.add_argument(
        "--version",
        action="version",
        version="[argparse.prog]%(prog)s[/] v[i]" + agenet_version + "[/]",
    )

    # Parse the command line arguments
    args = parser.parse_args()

    console.print(f"[{agenet_color}]agenet[/] v[i]{agenet_version}[/i]")

    try:

        # Create a shared counter for keeping tabs on the simulation progress
        # Type 'i' means signed integer
        counter = Value("i", 0)

        # Event for signalling the simulation to stop
        stop_event = Event()

        # At least one simulation argument is required to run the simulation
        sim_args = {
            "-f",
            "--frequency",
            "-e",
            "--num-events",
            "-r",
            "--num-runs",
            "-s",
            "--seed",
            "--num-bits",
            "--info-bits",
            "--power",
            "--distance",
            "--N0",
            "--num-bits-2",
            "--info-bits-2",
            "--power-2",
            "--distance-2",
            "--N0-2",
        }

        if len(set(sys.argv) & sim_args) == 0:
            parser.print_help()
            raise ValueError(
                "The agenet command requires at least one simulation parameter."
            )

        # Determine the total number of steps (parameter combinations)
        total_steps = (
            len(args.frequency)
            * len(args.num_events)
            * len(args.num_bits)
            * len(args.info_bits)
            * len(args.power)
            * len(args.distance)
            * len(args.N0)
            * len(args.num_bits_2)
            * len(args.info_bits_2)
            * len(args.power_2)
            * len(args.distance_2)
            * len(args.N0_2)
        )

        # Run the simulation within the context of a progress bar
        with Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("", total=total_steps)

            with ThreadPoolExecutor(max_workers=1) as executor:

                # Execute the simulation in a separate thread
                future = executor.submit(
                    multi_param_ev_sim,
                    num_runs=args.num_runs,
                    frequency=sorted(set(args.frequency)),
                    num_events=sorted(set(args.num_events)),
                    num_bits=sorted(set(args.num_bits)),
                    info_bits=sorted(set(args.info_bits)),
                    power=sorted(set(args.power)),
                    distance=sorted(set(args.distance)),
                    N0=sorted(set(args.N0)),
                    num_bits_2=sorted(set(args.num_bits_2)),
                    info_bits_2=sorted(set(args.info_bits_2)),
                    power_2=sorted(set(args.power_2)),
                    distance_2=sorted(set(args.distance_2)),
                    N0_2=sorted(set(args.N0_2)),
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
                    run_log.append(
                        RunLogMsg(
                            message="Simulation terminated early by user!",
                            msg_type=MsgType.WARNING,
                        )
                    )

                # Get the result after the task finishes
                results, param_error_log = future.result()

                # Log the time taken to run the simulation
                elapsed_time = progress.tasks[task].elapsed
                run_log.append(
                    RunLogMsg(
                        message=f"Elapsed simulation time: {elapsed_time:.2f} seconds",
                        msg_type=MsgType.INFO,
                    )
                )

        # Process output options
        if args.show_table:

            table = df_to_table(results)
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            console.print(table)

        if len(param_error_log) > 0:
            param_errors = [
                f"{len(param_error_log[s])} invalid parameter combinations due to: " + s
                for s in param_error_log.keys()
            ]

            run_log.extend([RunLogMsg(m, MsgType.WARNING) for m in param_errors])

        if args.save_csv:
            results.to_csv(args.save_csv, index=False)
            run_log.append(
                RunLogMsg(
                    message=f"Simulation results saved to `{args.save_csv}`",
                    msg_type=MsgType.INFO,
                )
            )

        if args.show_plot or args.save_plot is not None:
            aoi_vs_param: tuple[str, str, list[float | int]]
            num_var_params = 0
            for param_info in [
                ("frequency", "Frequency (Hz)", args.frequency),
                ("num_events", "Number of events", args.num_events),
                ("num_bits", "Number of bits", args.num_bits),
                ("info_bits", "Information bits", args.info_bits),
                ("power", "Transmission power (W)", args.power),
                ("distance", "Distance (m)", args.distance),
                ("N0", "N0 - Noise power (W)", args.N0),
                ("num_bits_2", "Number of bits in relay", args.num_bits_2),
                ("info_bits_2", "Information bits in relay", args.info_bits_2),
                ("power_2", "Transmission power in relay (W)", args.power_2),
                (
                    "distance_2",
                    "Distance from relay to destination (m)",
                    args.distance_2,
                ),
                ("N0_2", "N0 - Noise power in relay (W)", args.N0_2),
            ]:

                if len(param_info[2]) > 1:
                    num_var_params += 1
                    aoi_vs_param = param_info

            if num_var_params != 1:
                raise ValueError(
                    f"Unable to create plot: only 1 variable parameter is allowed, but there are {num_var_params}."
                )
            elif len(results) <= 1:
                raise ValueError("Unable to create plot: insufficient simulation data.")
            else:

                fig, ax = plt.subplots()
                aaoi_theory = results["aaoi_theory"]
                aaoi_sim = results["aaoi_sim"]
                if np.isinf(aaoi_theory).any() or np.isinf(aaoi_sim).any():
                    raise ValueError(
                        "Unable to create plot: some AAoI values are infinite."
                    )
                ax.plot(results[aoi_vs_param[0]], aaoi_theory, label="Theoretical")
                ax.plot(results[aoi_vs_param[0]], aaoi_sim, label="Simulation")
                ax.set_xlabel(aoi_vs_param[1])
                ax.set_ylabel("AAoI")
                ax.set_ylim((0, max([aaoi_theory.max(), aaoi_sim.max()]) * 1.05))
                ax.grid(True)
                ax.legend()
                if args.save_plot is not None:
                    fig.savefig(args.save_plot)
                    run_log.append(
                        RunLogMsg(
                            message=f"Simulation plot saved to `{args.save_plot}`",
                            msg_type=MsgType.INFO,
                        )
                    )

                if args.show_plot:
                    plot_to_display = ax

    except Exception as e:
        stop_event.set()
        if args.debug == 0:

            # Log the error message
            run_log.append(RunLogMsg(message=str(e), msg_type=MsgType.ERROR))

        elif args.debug == 1:
            err_console.print_exception()
        else:
            err_console.print_exception(show_locals=True)
        return_code = 1

    # Show run log
    run_log = sorted(run_log, key=lambda rlm: rlm.msg_type.code)
    for message, msg_type in run_log:
        msg_type.console.print(f" • {message}", style=msg_type.style)

    # Show plot if it exists and was requested by user
    if args.show_plot and plot_to_display is not None:
        plt.show()

    return return_code
