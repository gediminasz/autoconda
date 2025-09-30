"""Tests for autoconda CLI functionality."""

import tempfile
import pytest
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch

from autoconda.cli import main


def run_cli(args):
    """Helper function to run CLI with arguments and capture output."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    old_argv = sys.argv
    
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    sys.argv = ['autoconda'] + args
    
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
    exit_code, stdout, stderr = run_cli(['--version'])
    
    assert exit_code == 0
    assert 'autoconda 0.1.0' in stdout


def test_help_command():
    """Test help output."""
    exit_code, stdout, stderr = run_cli(['--help'])
    
    assert exit_code == 0
    assert 'Autoconda - Automatic conda environment management' in stdout
    assert 'activate' in stdout
    assert 'run' in stdout


def test_info_command_with_valid_environment():
    """Test info command with valid environment.yml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yml"
        env_content = """
name: test-info-env
dependencies:
  - python=3.9
  - numpy
channels:
  - conda-forge
"""
        env_file.write_text(env_content)
        
        exit_code, stdout, stderr = run_cli(['info', '--path', tmpdir])
        
        assert exit_code == 0
        assert 'Environment file:' in stdout
        assert 'Environment name: test-info-env' in stdout
        assert 'Dependencies: 2 items' in stdout
        assert 'Channels: conda-forge' in stdout


def test_info_command_no_environment():
    """Test info command when no environment.yml exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code, stdout, stderr = run_cli(['info', '--path', tmpdir])
        
        assert exit_code == 1
        assert 'No environment.yml file found' in stdout


def test_info_command_no_name():
    """Test info command when environment.yml has no name."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yml"
        env_content = """
dependencies:
  - python=3.9
"""
        env_file.write_text(env_content)
        
        exit_code, stdout, stderr = run_cli(['info', '--path', tmpdir])
        
        assert exit_code == 1
        assert 'No environment name specified' in stdout


def test_activate_command_no_environment():
    """Test activate command when no environment.yml exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code, stdout, stderr = run_cli(['activate', '--path', tmpdir])
        
        assert exit_code == 1
        assert 'No environment.yml file found' in stderr


def test_run_command_no_environment():
    """Test run command when no environment.yml exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        exit_code, stdout, stderr = run_cli(['run', '--path', tmpdir, 'echo', 'test'])
        
        assert exit_code == 1
        assert 'No environment.yml file found' in stderr


def test_run_command_no_args():
    """Test run command without arguments."""
    exit_code, stdout, stderr = run_cli(['run'])
    
    assert exit_code == 2
    assert 'No command specified' in stderr