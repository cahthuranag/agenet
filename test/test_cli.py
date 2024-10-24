"""Tests for the command-line script."""

import importlib.metadata
import signal
import subprocess
import sys
import time

import pytest
import matplotlib.pyplot as plt

agenet_cmd = "agenet"
elapsed_str = "Elapsed simulation time: "


@pytest.mark.parametrize("help_param", ["--help", "-h"])
def test_help_message(script_runner, help_param):
    """Test that help is shown when requested."""
    ret = script_runner.run([agenet_cmd, help_param])
    assert ret.success
    assert f"Usage: {agenet_cmd}" in ret.stdout


def test_empty(script_runner):
    """Test that help is shown when no params are given."""
    ret = script_runner.run([agenet_cmd])
    assert ret.returncode == 1
    assert f"Usage: {agenet_cmd}" in ret.stdout


def test_invalid_args(script_runner):
    """Test that invalid arguments are marked as such."""
    inv_arg = "--invalid-arg"
    ret = script_runner.run([agenet_cmd, inv_arg])
    assert ret.returncode == 2
    assert f"unrecognized arguments: {inv_arg}" in ret.stderr


def test_version(script_runner):
    """Test that the --version option works appropriately."""
    agenet_version = importlib.metadata.version("agenet")
    ret = script_runner.run([agenet_cmd, "--version"])
    assert ret.success
    assert f"{agenet_cmd} v{agenet_version}" in ret.stdout


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Does not work on Windows")
def test_keyboard_interrupt():
    """Test a keyboard interrupt."""
    # Start the subprocess that runs the function in a separate Python interpreter
    process = subprocess.Popen(
        [
            agenet_cmd,
            "--distance",
            *[str(f) for f in range(10, 1000)],
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Give the subprocess some time to run
    time.sleep(2)

    # Send SIGINT to the subprocess to simulate a CTRL+C (KeyboardInterrupt)
    process.send_signal(signal.SIGINT)

    # Wait for the subprocess to terminate
    stdout, _ = process.communicate()

    # Check if the subprocess caught the KeyboardInterrupt and terminated correctly
    assert "Simulation terminated early by user!" in stdout
    assert elapsed_str in stdout
    assert process.returncode == 0


@pytest.mark.parametrize("table_param", ["--show-table", "-t"])
def test_table(monkeypatch, script_runner, table_param):
    """Test if a table is produced when requested."""
    # Coerce Rich into thinking it's outputting to a wide console with no color
    monkeypatch.setenv("NO_COLOR", "")
    monkeypatch.setenv("COLUMNS", "300")

    # Run the script
    ret = script_runner.run(
        [agenet_cmd, table_param, "--distance", "100", "200", "300"]
    )

    # Assert that the table was shown
    assert ret.success
    assert "freq" in ret.stdout
    assert "num_" in ret.stdout
    assert "info_" in ret.stdout
    assert "powe" in ret.stdout
    assert "dist" in ret.stdout
    assert "N0" in ret.stdout
    assert elapsed_str in ret.stdout


@pytest.mark.parametrize(
    "valid_params",
    [
        ["--frequency", "2500000000"],
        ["-f", "750000000"],
        ["-f", "250000000", "500000000", "750000000"],
        ["--num-events", "25"],
        ["-e", "5", "35", "51"],
        ["--num-runs", "10"],
        ["-r", "12"],
        ["-s", "12334"],
        ["--seed", "3546"],
        ["--num-bits", "500"],
        ["--num-bits", "400", "500", "600"],
        ["--info-bits", "305"],
        ["--info-bits", "220", "300", "380"],
        ["--power", "0.008"],
        ["--power", "0.001", "0.003", "0.005", "0.007", "0.009"],
        ["--N0", "1e-13"],
        ["--N0", "1e-13", "2e-13", "3e-13", "4e-13", "5e-13"],
        ["--num-bits-2", "600"],
        ["--num-bits-2", "500", "600", "700", "800"],
        ["--info-bits-2", "305"],
        ["--info-bits-2", "280", "305", "325"],
        ["--power-2", "0.006"],
        ["--power-2", "0.001", "0.002", "0.003", "0.004", "0.005"],
        ["--N0-2", "5e-14"],
        ["--N0-2", "5e-14", "6e-14", "7e-14", "8e-14", "9e-14"],
    ],
)
def test_valid_params(script_runner, valid_params):
    """Test that valid parameters don't produce errors."""
    ret = script_runner.run([agenet_cmd, *valid_params])
    assert ret.success
    assert elapsed_str in ret.stdout


def test_invalid_param_combos(script_runner):
    """Test that invalid parameter combinations are caught."""
    ret = script_runner.run(
        [
            agenet_cmd,
            "-f",
            "-10",
            "2500000000",
            "--num-bits",
            "300",
            "350",
            "400",
            "450",
            "--info-bits",
            "310",
            "390",
            "410",
            "480",
        ]
    )
    assert ret.success
    assert "invalid parameter combinations due to:" in ret.stdout
    assert elapsed_str in ret.stdout


def test_save_csv(tmp_path, script_runner):
    """Test if CSV file was successfully saved."""
    csv_file = tmp_path / "results.csv"

    ret = script_runner.run(
        [
            agenet_cmd,
            "--distance-2",
            *[str(f) for f in range(300, 310)],
            "--save-csv",
            str(csv_file),
        ]
    )

    assert ret.success
    assert csv_file.exists()
    assert csv_file.is_file()
    assert len(csv_file.read_text()) > 0
    assert elapsed_str in ret.stdout


def test_save_plot(tmp_path, script_runner):
    """Test if plot image was successfully saved."""
    img_file = tmp_path / "plot.png"

    ret = script_runner.run(
        [agenet_cmd, "--power", "0.001", "0.002", "0.003", "--save-plot", str(img_file)]
    )

    assert ret.success
    assert img_file.exists()
    assert img_file.is_file()
    assert len(img_file.read_bytes()) > 0
    assert elapsed_str in ret.stdout


def test_show_plot(monkeypatch, script_runner):
    """Test displaying the plot."""

    def mock_show():
        mock_show.was_called = True

    mock_show.was_called = False
    monkeypatch.setattr(plt, "show", mock_show)

    ret = script_runner.run(
        [agenet_cmd, "--power", "0.001", "0.002", "0.003", "--show-plot"]
    )

    assert mock_show.was_called, "plt.show() was not called"
    assert ret.success
    assert elapsed_str in ret.stdout


@pytest.mark.parametrize(
    "invalid_plot_params, error_msg",
    [
        (["--frequency", "-10", "-20", "-30"], "insufficient simulation data"),
        (["--N0", "2e-13"], "only 1 variable parameter is allowed, but there are 0"),
        (
            ["--power", "0.001", "0.002", "--distance-2", "300", "400"],
            "only 1 variable parameter is allowed, but there are 2",
        ),
        (["-f", "1e13", "2e13", "5e13"], "some AAoI values are infinite"),
    ],
)
def test_plot_errors(monkeypatch, script_runner, invalid_plot_params, error_msg):
    """Test if plot creation errors are raised."""
    # Say to Rich that we have a 300-column terminal (required for Windows)
    monkeypatch.setenv("NO_COLOR", "")
    monkeypatch.setenv("COLUMNS", "300")

    ret = script_runner.run([agenet_cmd, "--show-plot", *invalid_plot_params])

    assert ret.returncode == 1
    assert "Unable to create plot" in ret.stderr
    assert error_msg in ret.stderr
    assert elapsed_str in ret.stdout
