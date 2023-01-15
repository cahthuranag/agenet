import pytest
from agenet.maincom import main
import matplotlib.pyplot as plt 

def test_main_empty():
 assert not len(main()) == 0, "the list is non empty"



@pytest.fixture(scope='function')
def plot_fn():
    def _plot(points):
        plt.plot(points)
        yield plt.show()
        plt.close('all')
    return _plot


def test_plot_fn(plot_fn):
    points = [1, 2, 3]
    plot_fn(points)
    assert True