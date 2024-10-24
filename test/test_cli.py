"""Tests for the command-line script."""

import importlib.metadata

import pytest

agenet_cmd = "agenet"


@pytest.mark.parametrize("help_param", ["--help", "-h"])
def test_help_message(script_runner, help_param):
    """Test that help is shown when requested."""
    ret = script_runner.run([agenet_cmd, help_param])
    assert ret.success
    assert f"Usage: {agenet_cmd}" in ret.stdout


def test_empty(script_runner):
    """Test that help is shown when no params are given."""
    ret = script_runner.run([agenet_cmd])
    assert ret.returncode == 1
    assert f"Usage: {agenet_cmd}" in ret.stdout


def test_invalid_args(script_runner):
    """Test that invalid arguments are marked as such."""
    inv_arg = "--invalid-arg"
    ret = script_runner.run([agenet_cmd, inv_arg])
    assert ret.returncode == 2
    assert f"unrecognized arguments: {inv_arg}" in ret.stderr


def test_version(script_runner):
    """Test that the --version option works appropriately."""
    agenet_version = importlib.metadata.version("agenet")
    ret = script_runner.run([agenet_cmd, "--version"])
    assert ret.success
    assert f"{agenet_cmd} v{agenet_version}" in ret.stdout
