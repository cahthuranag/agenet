import matplotlib.pyplot as plt
from maincom import main, run_main

# define the function with five variables
# def my_function(a, b, c, d, e):
# do some calculations and return two values
# simulated_value = a + b * c - d / e
# theoretical_value = a * c**2 - b**2 + d * e
# return simulated_value, theoretical_value


# create a range of values for each variable except the one being plotted
num_nodes_vals = [1, 2, 3, 4, 5]
active_prob_vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
n_vals = [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
k_vals = [50, 100, 150, 200, 250]
P_vals = [
    400 * (10**-3),
    450 * (10**-3),
    500 * (10**-2),
    600 * (10**-2),
    700 * (10**-2),
]

# specify the constant values for each variable
num_nodes_const = 2
acative_prob_vals_const = 0.5
n_const = 300
k_const = 100
P_const = 500 * (10**-2)

# loop through each variable and plot its values against the two outputs
for i, (var_name, var_vals) in enumerate(
    zip(
        [
            "number of nodes",
            "active probability",
            "block length",
            "update size",
            "Power",
        ],
        [num_nodes_vals, active_prob_vals, n_vals, k_vals, P_vals],
    )
):
    # create a list of the constant values with the loop variable set to None
    const_vals = [num_nodes_const, acative_prob_vals_const, n_const, k_const, P_const]
    const_vals[i] = None

    # create a new figure and plot the simulated and theoretical values with the constant values
    fig, ax = plt.subplots()
    ax.plot(
        var_vals,
        [
            run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))[0]
            for val in var_vals
        ],
        label="Theoretical",
    )
    ax.plot(
        var_vals,
        [
            run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))[1]
            for val in var_vals
        ],
        label="Simulated",
    )
    ax.set_xlabel(var_name)
    ax.legend()
    ax.set_title(f"Plot of Simulated and Theoretical Values with respect to {var_name}")

    # adjust the x and y-axis limits based on the minimum and maximum values in the plotted variable and output
    ax.set_xlim(min(var_vals), max(var_vals))
    ax.set_ylim(
        min(
            min(
                [
                    run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))
                    for val in var_vals
                ]
            )
        ),
        max(
            max(
                [
                    run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))
                    for val in var_vals
                ]
            )
        ),
    )

plt.show()
