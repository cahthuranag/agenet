def plot(numevnts=1000, numruns=100):
    import matplotlib
    #matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from agenet.maincom import main, run_main

    # create a range of values for each variable except the one being plotted
    num_nodes_vals = [1, 2, 3, 4, 5]
    active_prob_vals = [0.1, 0.15, 0.2, 0.25]
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
    acative_prob_vals_const = 0.5
    n_const = 150
    k_const = 100
    P_const = 2 * (10**-3)

    # initialize the minimum and maximum values for the x and y-axes
    x_min, x_max = float("inf"), float("-inf")
    y_min, y_max = float("inf"), float("-inf")

    for i, (var_name, var_vals) in enumerate(
        zip(
            [
                "number of nodes",
                "active probability",
                "block length",
                "update size",
                "Power",
            ],
            [
                num_nodes_vals,
                active_prob_vals,
                n_vals,
                k_vals,
                P_vals,
                numevnts,
                numruns,
            ],
        )
    ):
        # create a list of the constant values with the loop variable set to None
        const_vals = [
            num_nodes_const,
            acative_prob_vals_const,
            n_const,
            k_const,
            P_const,
            numevnts,
            numruns,
        ]
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
        ax.set_title(
            f"Plot of Simulated and Theoretical Values with respect to {var_name}"
        )

        # update the minimum and maximum values for the x and y-axes
        x_min = min(x_min, min(var_vals))
        x_max = max(x_max, max(var_vals))
        y_min = min(
            y_min,
            min(
                min(
                    [
                        run_main(*(const_vals[:i] + [val] + const_vals[i + 1 :]))
                        for val in var_vals
                    ]
                )
            ),
        )
        y_max = max(
            y_max,
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

    # set the x and y-axis limits based on the updated minimum and maximum values
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
