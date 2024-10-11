"""Tests for the CLI module."""

import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from agenet.cli import _main

# Helper function to setup mock args
def setup_mock_args(**kwargs):
    """Setup mock args for testing."""
    default_args = {
        "d": [100],
        "N0": [1e-13],
        "fr": [6e6],
        "num_events": [50],
        "num_nodes": [5],
        "active_prob": [0.2],
        "n": [150],
        "k": [50],
        "P": [8e-2],
        "num_runs": 10,
        "seed": None,
        "quiet": False,
        "blockerror": False,
        "snr": False,
        "csv": None,
    }
    default_args.update(kwargs)
    mock_args = MagicMock(**default_args)
    return mock_args

@pytest.fixture
def mock_dependencies():
    """Fixture for mocking dependencies."""
    with patch("agenet.cli.argparse.ArgumentParser.parse_args") as mock_parse_args, \
         patch("agenet.cli.snr_th") as mock_snr_th, \
         patch("agenet.cli.block_error_th") as mock_block_error_th, \
         patch("agenet.cli.multi_param_ev_sim") as mock_multi_param_ev_sim, \
         patch("pandas.DataFrame.to_csv") as mock_to_csv:
        yield {
            "mock_parse_args": mock_parse_args,
            "mock_snr_th": mock_snr_th,
            "mock_block_error_th": mock_block_error_th,
            "mock_multi_param_ev_sim": mock_multi_param_ev_sim,
            "mock_to_csv": mock_to_csv,
        }

@pytest.mark.xfail(reason="FIX ME")
def test_main_default_behavior(mock_dependencies, capsys):
    """Test the default behavior of the main function."""
    mock_args = setup_mock_args()
    mock_dependencies["mock_parse_args"].return_value = mock_args
    mock_result = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_dependencies["mock_multi_param_ev_sim"].return_value = mock_result

    _main()

    mock_dependencies["mock_multi_param_ev_sim"].assert_called_once_with(
        d=[100], N0=[1e-13], fr=[6e6], numevnts=[50], num_nodes=[5],
        active_prob=[0.2], n=[150], k=[50], P=[8e-2], numruns=10, seed=None
    )
    captured = capsys.readouterr()
    assert "col1" in captured.out and "col2" in captured.out

@pytest.mark.xfail(reason="FIX ME")
def test_main_with_snr(mock_dependencies, capsys):
    """Test the behavior of the main function with the --snr flag."""
    mock_args = setup_mock_args(snr=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args
    mock_dependencies["mock_snr_th"].return_value = 10.0

    _main()

    mock_dependencies["mock_snr_th"].assert_called_once_with(1e-13, 100, 8e-2, 6e6)
    captured = capsys.readouterr()
    assert "Theoretical SNR: 10.0" in captured.out

def test_main_with_blockerror(mock_dependencies, capsys):
    """Test the behavior of the main function with the --blockerror flag."""
    mock_args = setup_mock_args(blockerror=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args
    mock_dependencies["mock_block_error_th"].return_value = 0.01

    _main()

    mock_dependencies["mock_block_error_th"].assert_called_once()
    captured = capsys.readouterr()
    assert "Theoretical Block Error Rate: 0.01" in captured.out

def test_main_with_csv(mock_dependencies, tmp_path):
    """Test the behavior of the main function with the --csv flag."""
    csv_file = tmp_path / "output.csv"
    mock_args = setup_mock_args(csv=str(csv_file))
    mock_dependencies["mock_parse_args"].return_value = mock_args
    mock_result = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_dependencies["mock_multi_param_ev_sim"].return_value = mock_result

    _main()

    mock_dependencies["mock_to_csv"].assert_called_once_with(str(csv_file), index=False)

def test_main_with_seed(mock_dependencies):
    """Test the behavior of the main function with a specified seed."""
    mock_args = setup_mock_args(seed=42)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    _, kwargs = mock_dependencies["mock_multi_param_ev_sim"].call_args
    assert kwargs.get("seed") == 42

def test_main_quiet_mode(mock_dependencies, capsys):
    """Test the behavior of the main function in quiet mode."""
    mock_args = setup_mock_args(quiet=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args
    mock_result = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_dependencies["mock_multi_param_ev_sim"].return_value = mock_result

    _main()

    captured = capsys.readouterr()
    assert not captured.out  # Check that nothing was printed

@pytest.mark.xfail(reason="FIX ME")
def test_main_multiple_parameters(mock_dependencies):
    """Test the behavior of the main function with multiple parameter values."""
    mock_args = setup_mock_args(
        d=[100, 200],
        N0=[1e-13, 2e-13],
        num_nodes=[5, 10],
        active_prob=[0.2, 0.3],
        n=[150, 200],
        k=[50, 75],
        P=[8e-2, 9e-2]
    )
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_multi_param_ev_sim"].assert_called_once_with(
        d=[100, 200], N0=[1e-13, 2e-13], fr=[6e6], numevnts=[50],
        num_nodes=[5, 10], active_prob=[0.2, 0.3], n=[150, 200],
        k=[50, 75], P=[8e-2, 9e-2], numruns=10, seed=None
    )

def test_main_no_output_action(mock_dependencies, capsys):
    """Test the main function when no output action is specified."""
    mock_args = setup_mock_args(quiet=True, snr=False, blockerror=False, csv=None)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_multi_param_ev_sim"].assert_called_once()
    captured = capsys.readouterr()
    assert not captured.out  # Check that nothing was printed

def test_main_all_flags(mock_dependencies, capsys, tmp_path):
    """Test the main function with all flags set."""
    csv_file = tmp_path / "output.csv"
    mock_args = setup_mock_args(snr=True, blockerror=True, csv=str(csv_file))
    mock_dependencies["mock_parse_args"].return_value = mock_args
    mock_dependencies["mock_snr_th"].return_value = 10.0
    mock_dependencies["mock_block_error_th"].return_value = 0.01
    mock_result = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_dependencies["mock_multi_param_ev_sim"].return_value = mock_result

    _main()

    mock_dependencies["mock_snr_th"].assert_called_once()
    mock_dependencies["mock_block_error_th"].assert_called_once()
    mock_dependencies["mock_multi_param_ev_sim"].assert_called_once()
    mock_dependencies["mock_to_csv"].assert_called_once_with(str(csv_file), index=False)
    captured = capsys.readouterr()
    assert "Theoretical SNR: 10.0" in captured.out
    assert "Theoretical Block Error Rate: 0.01" in captured.out
    assert "col1" in captured.out and "col2" in captured.out
