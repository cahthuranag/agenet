import os
import subprocess
import sys

import pytest

from agenet import main

# define test cases
test_cases = [
    (2, 0.9, 300, 100, 10**-3, 1000),  # test case 1
    (4, 0.5, 500, 50, 50**-3, 1000),  # test case 2
]


# define pytest function to test main function with multiple test cases
@pytest.mark.parametrize(
    "num_nodes, active_prob, n, k, P,numevents", test_cases
)
def test_main(num_nodes, active_prob, n, k, P, numevents):
    # call the main function
    result = main(num_nodes, active_prob, n, k, P, numevents)
    # assert that the result is not None
    assert result is not None

def test_command_line_arguments():
    # Define sample command-line arguments
    num_nodes = 2
    active_prob = 0.5
    n = 200
    k = 150
    P = 0.1
    numevents = 1000
    numruns = 1

    # Run the script with the sample command-line arguments
    script_path = os.path.abspath("agenet/maincom.py")
    command = (
        f"python {script_path} "
        f"--num_nodes {num_nodes} "
        f"--active_prob {active_prob} "
        f"--n {n} "
        f"--k {k} "
        f"--P {P} "
        f"--numevents {numevents} "
        f"--numruns {numruns}"
    )

    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )

    # Check if the script ran successfully (return code 0)
    assert result.returncode == 0
    # Check if there is some output (stdout is not empty)
    assert result.stdout.strip() != ""
