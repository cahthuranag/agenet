import pytest

from agenet.maincom import main, main_fun
from io import StringIO
import sys

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




def test_main_fun(capsys):
    # Set up the arguments
    sys.argv = [
        'program_name.py', 
        '--num_nodes', '2', 
        '--active_prob', '0.5', 
        '--n', '200', 
        '--k', '150', 
        '--P', '0.1', 
        '--numevents', '10', 
        '--numruns', '1'
    ]
    
    # Run the main function
    main_fun()

    # Capture the output
    captured = capsys.readouterr()

    # Check if the output contains the expected string
    assert "Theoretical AAoI:" in captured.out
    assert "Simulation AAoI:" in captured.out
