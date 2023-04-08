import pytest
import matplotlib

# Use a non-GUI backend for matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


@pytest.mark.mpl_image_compare
def test_plot_does_not_show_plots():
    from agenet.maincom import main, run_main
    from agenet.plot import plot

    # Set the input values
    numevnts = 10
    numruns = 10

    # Call the plot function
    fig = plot(numevnts, numruns)

    # Compare the resulting plot to a reference image
    # This image should be stored in the same directory as this test script
    # and named "test_plot_does_not_show_plots.png"
    # The tolerance parameter specifies the maximum RMS pixel difference allowed
    # between the resulting plot and the reference image
    return fig
