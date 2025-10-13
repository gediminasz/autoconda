"""Tests for autoconda CLI functionality."""

import sys
import tempfile
from io import StringIO

from autoconda.cli import main


def run_cli(args):
    """Helper function to run CLI with arguments and capture output."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    old_argv = sys.argv

    sys.stdout = StringIO()
    sys.stderr = StringIO()
    sys.argv = ["autoconda"] + args

    exit_code = 0
    try:
        main()
    except SystemExit as e:
        exit_code = e.code if e.code is not None else 0

    stdout_value = sys.stdout.getvalue()
    stderr_value = sys.stderr.getvalue()

    sys.stdout = old_stdout
    sys.stderr = old_stderr
    sys.argv = old_argv

    return exit_code, stdout_value, stderr_value


def test_version_command():
    """Test --version flag."""
    exit_code, stdout, stderr = run_cli(["--version"])

    assert exit_code == 0
    assert "autoconda 0.1.0" in stdout


def test_help_command():
    """Test help output."""
    exit_code, stdout, stderr = run_cli(["--help"])

    assert exit_code == 0
    assert "Autoconda - Automatic conda environment management" in stdout


def test_run_command_no_environment():
    """Test run command when no environment.yml exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code, stdout, stderr = run_cli(["--path", tmpdir, "echo", "test"])

        assert exit_code == 1
        assert "No environment.yml file found" in stderr


def test_run_command_with_subcommand_no_environment():
    """Test run subcommand when no environment.yml exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code, stdout, stderr = run_cli(["run", "--path", tmpdir, "echo", "test"])

        assert exit_code == 1
        assert "No environment.yml file found" in stderr


def test_run_command_no_args():
    """Test run command without arguments."""
    exit_code, stdout, stderr = run_cli([])

    assert exit_code == 0
    assert "usage:" in stdout or "Autoconda" in stdout
