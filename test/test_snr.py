import os
import subprocess
import sys

from agenet import snr


def test_snr():
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr= 6 * (10**9)
    result = snr(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0


def test_snr_th():
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    fr= 6 * (10**9)
    result = snr(N0, d, P, fr)
    assert isinstance(result, float)
    assert result >= 0

def test_command_line_arguments():
    script_path = os.path.abspath("agenet/snr.py")
    # Use the value 6000000000 instead of 6*(10**9) or enclose the expression in quotes
    command = f"python {script_path} -N0 0.1 -d 100 -P 1 -fr 6000000000"
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True
    )
    assert "SNR:" in result.stdout
    assert "Theoretical SNR:" in result.stdout

