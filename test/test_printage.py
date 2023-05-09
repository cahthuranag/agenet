# Tests for printage.py
from agenet.printage import printage


def test_printage(capsys):
    printage(numevnts=10, numruns=10)
    captured = capsys.readouterr()
    assert "number of nodes" in captured.out
    assert "active probability" in captured.out
    assert "block length" in captured.out
    assert "update size" in captured.out
    assert "Power" in captured.out
    assert "Theoretical" in captured.out
    assert "Simulated" in captured.out
