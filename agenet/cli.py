"""Command-line interface for AgeNet."""

from __future__ import annotations

import argparse
from enum import Enum
import importlib.metadata
import sys
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value
from threading import Event
from time import sleep

import matplotlib.pyplot as plt
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich_argparse import RichHelpFormatter
from rich_tools import df_to_table

from .simulation import multi_param_ev_sim


class __PanelType(Enum):
    """Different types of text panel."""

    ALERT = (1, "Alert", "red", "bold bright_red")
    WARNING = (2, "Warning", "orange_red1", "bold dark_orange")

    # Custom initializer to unpack the tuple
    def __init__(self, code, title, border_style, text_style):
        self.code = code
        self.title = title
        self.border_style = border_style
        self.text_style = text_style


def __panel(ptype: __PanelType, text: str) -> Panel:
    """Display a text panel."""
    # Create the error text with bold red color
    styled_text = Text(text, style=ptype.text_style)

    # Wrap the text in a panel to clearly differentiate from the
    # remaining output
    return Panel.fit(
        styled_text,
        title=ptype.title,
        title_align="left",
        border_style=ptype.border_style,
        padding=(1, 2),
    )


def _main() -> int:
    """Function invoked when running the agenet command at the terminal."""
    # Initialize a Rich console for enhanced terminal output
    console = Console()

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
        description="AgeNet is a Python package to estimate the Age of Information in cooperative wireless networks",
        formatter_class=lambda prog: RichHelpFormatter(prog, console=console),
    )

    # Global simulation parameters
    general_group = parser.add_argument_group("General simulation parameters", "")

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
        "Node (or source node) simulation parameters", ""
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
        "Relay-specific simulation parameters (if different than source node)",
        "",
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
    output_group = parser.add_argument_group("Output specification", "")

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
        type=str,
        default="",
        metavar="IMAGE_FILE",
        help="Save plot to file (only valid if exactly one parameter varies, extension determines file type)",
    )

    output_group.add_argument(
        "--debug",
        choices=["0", "1", "2"],
        default="0",
        help="Level of debugging report if an error occurs (default: %(default)s)",
    )

    output_group.add_argument(
        "--version",
        action="version",
        version="[argparse.prog]%(prog)s[/] v[i]"
        + importlib.metadata.version("agenet")
        + "[/]",
    )

    try:

        # Parse the command line arguments
        args = parser.parse_args()

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
                "The agenet command requires at least one simulation argument"
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
        with Progress() as progress:
            task = progress.add_task("[white]Simulating...", total=total_steps)

            with ThreadPoolExecutor(max_workers=1) as executor:

                # Execute the simulation in a separate thread
                future = executor.submit(
                    multi_param_ev_sim,
                    num_runs=args.num_runs,
                    frequency=args.frequency,
                    num_events=args.num_events,
                    num_bits=args.num_bits,
                    info_bits=args.info_bits,
                    power=args.power,
                    distance=args.distance,
                    N0=args.N0,
                    num_bits_2=args.num_bits_2,
                    info_bits_2=args.info_bits_2,
                    power_2=args.power_2,
                    distance_2=args.distance_2,
                    N0_2=args.N0_2,
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
                    err_console.print(
                        __panel(
                            __PanelType.WARNING, "Simulation terminated early by user!"
                        )
                    )

                # Get the result after the task finishes
                results, param_error_log = future.result()

        # Process output options
        if args.show_table:

            table = df_to_table(results)
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            console.print(table)

        if len(param_error_log) > 0:
            pel_str = "\n".join(["- " + s for s in param_error_log])
            errors_to_render = Markdown(
                "**Invalid parameter combinations which were not simulated:**\n"
                + pel_str
            )
            console.print(errors_to_render)

        if args.save_csv:
            results.to_csv(args.save_csv, index=False)
            console.print(f"Simulation results saved to {args.save_csv}")

        if args.show_plot or len(args.save_plot) > 0:
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
                ("num_bits_2", "Number of bits at relay/AP", args.num_bits_2),
                ("info_bits_2", "Information bits at relay/AP", args.info_bits_2),
                ("power_2", "Transmission power at relay/AP (W)", args.power_2),
                (
                    "distance_2",
                    "Distance from relay/AP to destination (m)",
                    args.distance_2,
                ),
                ("N0_2", "N0 - Noise power at relay/AP (W)", args.N0_2),
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
                ax.set_ylim((0, max([aaoi_theory.max(), aaoi_sim.max()]) * 1.05))
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

            # Print the error panel to the console
            err_console.print()
            err_console.print(__panel(__PanelType.ALERT, str(e)))

        elif args.debug == "1":
            err_console.print_exception()
        else:
            err_console.print_exception(show_locals=True)
        return 1

    return 0
