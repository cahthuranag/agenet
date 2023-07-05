import matplotlib.pyplot as plt

from agenet.plot import plot


def test_plot():
    # call the function to be tested
    plot(numevnts=500, numruns=1)

    # assert that the plot is not displayed
    assert len(plt.get_fignums()) == 5
    plt.close("all")
