import pytest
from agenet.av_age import average_age_of_information_fn


# def test_av_age_func_values():
#     assert av_age_func([2,3,4,5], [1,2,3,4]) == 1.3
@pytest.mark.parametrize("v,T, expected", [([2, 3, 4, 5], [1, 2, 3, 4], 1.3)])
def test_av_age_func_values(v, T, expected):
    age, _, _ = average_age_of_information_fn(v, T, 0.1)
    assert round(age, 1) == expected


@pytest.fixture(scope="function")
def plot_fn():
    def _plot(points):
        plt.plot(points)
        yield plt.show()
        plt.close("all")

    return _plot


def test_plot_fn(plot_fn):
    points = [1, 2, 3]
    plot_fn(points)
    assert True


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
