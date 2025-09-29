"""Tests for autoconda CLI functionality."""

import tempfile
import pytest
from pathlib import Path
from click.testing import CliRunner

from autoconda.cli import main


def test_version_command():
    """Test --version flag."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    
    assert result.exit_code == 0
    assert 'autoconda 0.1.0' in result.output


def test_help_command():
    """Test help output."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    
    assert result.exit_code == 0
    assert 'Autoconda - Automatic conda environment management' in result.output
    assert 'activate' in result.output
    assert 'run' in result.output


def test_info_command_with_valid_environment():
    """Test info command with valid environment.yml."""
    runner = CliRunner()
    
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
        
        result = runner.invoke(main, ['info', '--path', tmpdir])
        
        assert result.exit_code == 0
        assert 'Environment file:' in result.output
        assert 'Environment name: test-info-env' in result.output
        assert 'Dependencies: 2 items' in result.output
        assert 'Channels: conda-forge' in result.output


def test_info_command_no_environment():
    """Test info command when no environment.yml exists."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(main, ['info', '--path', tmpdir])
        
        assert result.exit_code == 1
        assert 'No environment.yml file found' in result.output


def test_info_command_no_name():
    """Test info command when environment.yml has no name."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yml"
        env_content = """
dependencies:
  - python=3.9
"""
        env_file.write_text(env_content)
        
        result = runner.invoke(main, ['info', '--path', tmpdir])
        
        assert result.exit_code == 1
        assert 'No environment name specified' in result.output


def test_activate_command_no_environment():
    """Test activate command when no environment.yml exists."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(main, ['activate', '--path', tmpdir])
        
        assert result.exit_code == 1
        assert 'No environment.yml file found' in result.output


def test_run_command_no_environment():
    """Test run command when no environment.yml exists."""
    runner = CliRunner()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(main, ['run', '--path', tmpdir, 'echo', 'test'])
        
        assert result.exit_code == 1
        assert 'No environment.yml file found' in result.output


def test_run_command_no_args():
    """Test run command without arguments."""
    runner = CliRunner()
    result = runner.invoke(main, ['run'])
    
    assert result.exit_code == 2  # Click returns 2 for usage errors
    assert 'Usage:' in result.output