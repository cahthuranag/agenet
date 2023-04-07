import matplotlib.pyplot as plt
import pytest

from agenet.maincom import main, run_main

# create test cases for the plot data
test_cases = [
    {
        "var_name": "number of nodes",
        "var_vals": [1, 2, 3, 4, 5],
        "const_vals": [2, 0.5, 150, 100, 0.002],
    },
    {
        "var_name": "active probability",
        "var_vals": [0.01, 0.1, 0.15, 0.2, 0.25],
        "const_vals": [2, 0.5, 150, 100, 0.002],
    },
    {
        "var_name": "block length",
        "var_vals": [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250],
        "const_vals": [2, 0.5, 150, 100, 0.002],
    },
    {
        "var_name": "update size",
        "var_vals": [50, 60, 70, 80, 90, 95, 100],
        "const_vals": [2, 0.5, 150, 100, 0.002],
    },
    {
        "var_name": "Power",
        "var_vals": [
            2 * (10**-3),
            3 * (10**-3),
            4 * (10**-3),
            5 * (10**-3),
            10 * (10**-3),
        ],
        "const_vals": [2, 0.5, 150, 100, 0.002],
    },
]


@pytest.mark.parametrize("test_case", test_cases)
def test_plot_data(test_case):
    var_name = test_case["var_name"]
    var_vals = test_case["var_vals"]
    const_vals = test_case["const_vals"]

    fig, ax = plt.subplots()

    # plot the simulated and theoretical values with the constant values
    theoretical_vals = [
        run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))[0] for val in var_vals
    ]
    simulated_vals = [
        run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))[1] for val in var_vals
    ]
    ax.plot(var_vals, theoretical_vals, label="Theoretical")
    ax.plot(var_vals, simulated_vals, label="Simulated")

    # check that the plotted data is correct
    assert ax.get_xlabel() == var_name
    assert (
        ax.get_title()
        == f"Plot of Simulated and Theoretical Values with respect to {var_name}"
    )
    assert ax.get_lines()[0].get_ydata().tolist() == theoretical_vals
    assert ax.get_lines()[1].get_ydata().tolist() == simulated_vals

    plt.close(fig)
