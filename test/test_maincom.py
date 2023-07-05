import pytest

from agenet.maincom import main

# define test cases
test_cases = [
    (2, 0.9, 300, 100, 10**-3, 1000),  # test case 1
    (4, 0.5, 500, 50, 50**-3, 1000),  # test case 2
]


# define pytest function to test main function with multiple test cases
@pytest.mark.parametrize("num_nodes, active_prob, n, k, P,numevents", test_cases)
def test_main(num_nodes, active_prob, n, k, P, numevents):
    # call the main function
    result = main(num_nodes, active_prob, n, k, P, numevents)
    # assert that the result is not None
    assert result is not None
