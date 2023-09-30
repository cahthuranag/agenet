from agenet.snr import snr,main

from io import StringIO
import sys


def test_snr():
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    result = snr(N0, d, P)
    assert isinstance(result, float)
    assert result >= 0


def test_snr_th():
    N0 = 1 * (10**-13)
    d = 1000
    P = 1 * (10**-3)
    result = snr(N0, d, P)
    assert isinstance(result, float)
    assert result >= 0



def test_main(capsys):
    # Set up the arguments
    sys.argv = ['program_name.py', '-N0', '0.1', '-d', '100', '-P', '1']
    
    # Run the main function
    main()

    # Capture the output
    captured = capsys.readouterr()

    # Check if the output contains the expected strings
    assert "SNR:" in captured.out
    assert "Theoretical SNR:" in captured.out
