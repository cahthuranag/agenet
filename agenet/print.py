import numpy as np
import math
import argparse

# import sys
import agenet
from scipy import special as sp
from agenet import av_age

# from av_age import validate
import matplotlib.pyplot as plt
from agenet import bler
import pandas as pd
import tabulate as tab
import itertools as intert


def printval():
    from agenet import maincom

    av_age_poisson_simulation, av_age_poisson_theoretical = maincom.main()
    all_data_age = list(zip(av_age_poisson_simulation, av_age_poisson_theoretical))
    print(
        tab.tabulate(
            all_data_age,
            tablefmt="psql",
            showindex=False,
            headers=["AAoI simulated", "AAoI theoritical"],
        )
    )


def ageplot():
    from agenet import maincom

    # from scipy.interpolate import spline
    from scipy.interpolate import make_interp_spline, BSpline

    genlambda, av_age_poisson_simulation, av_age_poisson_theoretical = maincom.main()
    xnew = np.linspace(np.array(genlambda).min(), np.array(genlambda).max(), 300)
    spl_sim = BSpline(genlambda, av_age_poisson_simulation, k=2)  # type: BSpline
    sim_smooth = spl_sim(xnew)
    spl_th = BSpline(genlambda, av_age_poisson_theoretical, k=2)  # type: BSpline
    th_smooth = spl_th(xnew)
    #  sim_smooth = bpline(genlambda, av_age_poisson_simulation, xnew)
    #  th_smooth = spline(genlambda, av_age_poisson_theoretical, xnew)
    plt.plot(xnew, sim_smooth, label="simulated")
    plt.plot(xnew, th_smooth, label="theoretical")
    plt.xlabel("Update generation rate")
    plt.ylabel("AAoI")
    plt.legend()
    plt.show()
