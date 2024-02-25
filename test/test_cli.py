import pytest
from unittest.mock import patch, MagicMock
from agenet.cli import _main


# Helper function to setup mock args
def setup_mock_args(**kwargs):
    default_args = {
        "num_nodes_const": 2,
        "active_prob_const": 0.5,
        "n_const": 150,
        "k_const": 100,
        "P_const": 2 * (10**-3),
        "d_const": 700,
        "N0_const": 1 * (10**-13),
        "fr_const": 6 * (10**9),
        "numevnts": 500,
        "numruns": 100,
        "quiet": False,
        "plots": False,
        "plots_folder": None,
        "blockerror": False,
        "snr": False,
        "csv_location": None,
        "num_nodes_vals": [1, 2, 3, 4, 5],
        "active_prob_vals": [0.1, 0.15, 0.2, 0.25],
        "n_vals": [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250],
        "k_vals": [50, 60, 70, 80, 90, 95, 100],
        "P_vals": [2 * (10**-3), 4 * (10**-3), 6 * (10**-3), 8 * (10**-3)],
    }
    default_args.update(kwargs)
    mock_args = MagicMock(**default_args)
    return mock_args


@pytest.fixture
def mock_dependencies():
    with patch(
        "agenet.cli.argparse.ArgumentParser.parse_args"
    ) as mock_parse_args, patch("agenet.cli.plot") as mock_plot, patch(
        "agenet.cli.generate_table"
    ) as mock_generate_table, patch(
        "agenet.cli.snr_th"
    ) as mock_snr_th, patch(
        "agenet.cli.blercal_th"
    ) as mock_blercal_th:
        yield {
            "mock_parse_args": mock_parse_args,
            "mock_plot": mock_plot,
            "mock_generate_table": mock_generate_table,
            "mock_snr_th": mock_snr_th,
            "mock_blercal_th": mock_blercal_th,
        }


# Test default behavior without specific flags
def test_main_default_behavior(mock_dependencies):
    mock_args = setup_mock_args()
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_generate_table"].assert_called_once()
    mock_dependencies["mock_plot"].assert_not_called()
    mock_dependencies["mock_snr_th"].assert_not_called()
    mock_dependencies["mock_blercal_th"].assert_not_called()


# Test behavior with --plots flag
def test_main_with_plots(mock_dependencies):
    mock_args = setup_mock_args(plots=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_plot"].assert_called_once()


# Test behavior with --snr flag
def test_main_with_snr(mock_dependencies):
    mock_args = setup_mock_args(snr=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_snr_th"].assert_called_once()


# Test behavior with --blockerror flag
def test_main_with_blockerror(mock_dependencies):
    mock_args = setup_mock_args(blockerror=True)
    mock_dependencies["mock_parse_args"].return_value = mock_args

    _main()

    mock_dependencies["mock_blercal_th"].assert_called_once()
