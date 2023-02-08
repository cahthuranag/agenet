def average_age_of_information_function(arrival_time, generation_times):
    import numpy as np
    import matplotlib.pyplot as plt
    import itertools
    from scipy.integrate import simpson
    import sys

    # arrival times of the packets
    received_times = arrival_time
    # departure times of the packets
    generation_timess = generation_times

    # check if number of arrival and departure times are equal and not zero
    if (
        np.size(generation_timess) != np.size(received_times)
        or np.size(generation_timess) == 0
        or np.size(received_times) == 0
    ):
        print(
            "Error: The number of elements in departure times and arrival times should be equal and non-zero"
        )
        sys.exit()

    # initializing an array to store the times
    times = np.append(generation_timess, (received_times[-1]))
    # adding a zero at the beginning of the times array
    times = np.append([0], times)

    # index to keep track of arrival times
    ii = 0
    offset = 0
    # creating an array to store the ages
    age = times.copy()
    agep = np.zeros(np.size(generation_timess))

    # length of the times array
    lent = len(times)
    # loop through the times array
    for i in range(1, lent):
        # if the current time is equal to an arrival time
        if times[i] == received_times[ii]:
            # store the departure time
            offset = generation_timess[ii]
            ii += 1
            # subtract the offset from the current time
            age[i] = age[i] - offset

    # size of the departure times array
    k = np.size(generation_timess)
    agep[0] = received_times[0]
    # loop through the departure times array
    for i in range(1, k):
        # calculate the difference between the arrival and departure times
        agep[i] = received_times[i] - generation_timess[i - 1]

    # repeat the times array twice
    new_times = np.repeat(times, 2)
    # concatenate the age values and age differences
    new_age_differences = np.append((age[1]), agep)
    # add a zero at the beginning of the new_age_differences array
    new_age_differences = np.append([0], new_age_differences)
    # flatten the two arrays into a single array
    final = list(itertools.chain.from_iterable(zip(new_age_differences, age)))

    # calculate the average age of information
    average_age = np.trapz(final, new_times) / np.amax(new_times)
    return average_age
