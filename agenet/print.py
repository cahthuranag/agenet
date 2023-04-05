from tabulate import tabulate
from maincom import main, run_main

# create a range of values for each variable except the one being tabled
num_nodes_vals = [1, 2, 3, 4, 5]
active_prob_vals = [0.01, 0.1, 0.15, 0.2, 0.25]
n_vals = [150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
k_vals = [50, 60, 70, 80, 90, 95, 100]
P_vals = [
    2 * (10**-3),
    3 * (10**-3),
    4 * (10**-3),
    5 * (10**-3),
    10 * (10**-3),
]

# specify the constant values for each variable
num_nodes_const = 2
active_prob_const = 0.5
n_const = 150
k_const = 100
P_const = 2 * (10**-3)
#
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
    const_vals = [num_nodes_const, active_prob_const, n_const, k_const, P_const]
    const_vals[i] = None

    # create the table headers
    headers = [var_name, "Theoretical", "Simulated"]

    # create a list of rows for the table
    table_rows = []
    for val in var_vals:
        theoretical, simulated = run_main(
            *(const_vals[:i] + [val] + const_vals[i + 1 :])
        )
        table_rows.append([val, theoretical, simulated])

    # print the table
    print(tabulate(table_rows, headers=headers, tablefmt="grid"))
    print("\n")
