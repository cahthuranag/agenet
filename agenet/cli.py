"""Command-line interface for AgeNet."""

from __future__ import annotations

import argparse
import importlib.metadata
import sys
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from multiprocessing import Value
from threading import Event
from time import sleep

import matplotlib.pyplot as plt
from rich import box
from rich.console import Console, Group, RenderableType
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, TimeElapsedColumn
from rich.text import Text
from rich.theme import Theme
from rich_argparse import RichHelpFormatter
from rich_tools import df_to_table

from .simulation import multi_param_ev_sim


class _SectionType(Enum):
    """Different types of text panel."""

    ERROR = (1, "Error", "bold bright_red", "red")
    WARNING = (2, "Warning", "bold dark_orange", "orange_red1")
    INFO = (3, "Information", "bold", "")

    # Custom initializer to unpack the tuple
    def __init__(self, code, title, title_style, text_style):
        self.code = code
        self.title = title
        self.title_style = title_style
        self.text_style = text_style


class _ProgressPanel(Progress):
    """Custom progress bar in a panel."""

    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks), box=box.SIMPLE)


def _section(
    sec_type: _SectionType, contents: RenderableType, title=None
) -> RenderableType:
    """Display a new section."""
    # If the contents are a pure string, style them according to the section type
    styled_contents = (
        Text(contents, style=sec_type.text_style)
        if isinstance(contents, str)
        else contents
    )

    # Is there a custom title?
    title = sec_type.title if title is None else title

    # Wrap the text in a panel to clearly differentiate from the
    # remaining output
    return Group(
        Text(title, style=sec_type.title_style),
        Panel(styled_contents, box=box.SIMPLE),
    )


def _main() -> int:
    """Function invoked when running the agenet command at the terminal."""
    # Configure Rich consoles for enhanced terminal output
    md_list_warn_theme = Theme(
        {
            "markdown.item.bullet": _SectionType.WARNING.title_style,
            "markdown.item": _SectionType.WARNING.text_style,
            "markdown.code": _SectionType.WARNING.text_style + " on bright_black",
        }
    )

    err_console = Console(stderr=True, theme=md_list_warn_theme)

    md_list_info_theme = Theme(
        {
            "markdown.item.bullet": _SectionType.INFO.title_style,
            "markdown.item": _SectionType.INFO.text_style,
            "markdown.code": _SectionType.INFO.text_style + " on bright_black",
        }
    )

    console = Console(theme=md_list_info_theme)

    console.print()

    # List of exported / saved files
    exports: list[str] = []

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
        err_console.print(_section(_SectionType.ERROR, message))
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
        version="[argparse.prog]%(prog)s[/] v[i]"
        + importlib.metadata.version("agenet")
        + "[/]",
    )

    # Parse the command line arguments
    args = parser.parse_args()

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
        with _ProgressPanel(
            TimeElapsedColumn(),
            *Progress.get_default_columns(),
            console=console,
            transient=False,
        ) as progress:
            console.print(Text("Simulation progress", style="bold"))
            task = progress.add_task("", total=total_steps)

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
                    err_console.print(
                        _section(
                            _SectionType.WARNING, "Simulation terminated early by user!"
                        )
                    )

                # Get the result after the task finishes
                results, param_error_log = future.result()

        # Process output options
        if args.show_table:

            table = df_to_table(results)
            table.row_styles = ["none", "dim"]
            table.box = box.SIMPLE_HEAD
            console.print(
                _section(_SectionType.INFO, table, title="Simulation results")
            )

        if len(param_error_log) > 0:
            pel_str = "\n".join(
                [
                    f"- {len(param_error_log[s])} invalid parameter combinations due to: "
                    + s
                    for s in param_error_log.keys()
                ]
            )
            errors_to_render = Markdown(pel_str)

            err_console.print(_section(_SectionType.WARNING, errors_to_render))

        if args.save_csv:
            results.to_csv(args.save_csv, index=False)
            exports.append(f"Simulation results saved to `{args.save_csv}`")

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
                raise ValueError(
                    f"Unable to create plot: insufficient simulation data."
                )
            else:
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
                ax.grid(True)
                ax.legend()
                if args.save_plot is not None:
                    fig.savefig(args.save_plot)
                    exports.append(f"Simulation plot saved to `{args.save_plot}`")
                if args.show_plot:
                    plot_to_display = ax

    except Exception as e:
        stop_event.set()
        if args.debug == 0:

            # Print the error panel to the console
            err_console.print(_section(_SectionType.ERROR, str(e)))

        elif args.debug == 1:
            err_console.print_exception()
        else:
            err_console.print_exception(show_locals=True)
        return_code = 1

    if len(exports) > 0:
        exp_str = "\n".join(["- " + s for s in exports])
        exports_to_render = Markdown(exp_str)

        console.print(
            _section(_SectionType.INFO, exports_to_render, title="Saved data")
        )

    # Show plot if it exists and was requested by user
    if args.show_plot and plot_to_display is not None:
        plt.show()

    return return_code
