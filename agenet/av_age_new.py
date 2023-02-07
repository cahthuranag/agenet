import numpy as np
from scipy.integrate import trapz


def av_age_func(v, T, lambha):
    p = lambha
    times = np.arange(0, v[0] + p, p)
    for i in range(1, len(v)):
        dummy = np.arange(v[i - 1], v[i] + p, p)
        times = np.concatenate((times, dummy))

    ii = 1
    offset = 0
    age = times

    for i in range(len(times)):
        if times[i] == v[ii]:
            offset = T[ii]
            ii = ii + 1
        age[i] = age[i] - offset

    av_age = trapz(age, times) / np.amax(times)
    return av_age


def printageex():

    av_age_fn = av_age_func([1000.0, 1001.0], [2.0, 3.0], 1)
    print(
        "Average age of information  when  time slots are [2,3,4,5], [1,2,3,4]:",
        av_age_fn,
    )
