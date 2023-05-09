import matplotlib
matplotlib.use('Agg')  # use Agg backend

from agenet.plot import plot

def test_plot():
    # call the function to be tested
    plot(numevnts=1000, numruns=1)

    # assert that the plot is not displayed
    import matplotlib.pyplot as plt
    assert len(plt.get_fignums()) == 0


