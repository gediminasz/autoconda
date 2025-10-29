"""Tests for autoconda environment parsing functionality."""

import tempfile
from pathlib import Path

import pytest

from autoconda.environment import (
    find_environment_file,
    get_conda_environment_name,
    get_environment_name,
    parse_environment_file,
)


def test_find_environment_file_in_current_dir():
    """Test finding environment.yml in current directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create environment.yml in temp directory
        env_file = Path(tmpdir) / "environment.yml"
        env_file.write_text("name: test-env\n")

        # Should find the file
        result = find_environment_file(tmpdir)
        assert result == env_file


def test_find_environment_file_in_parent_dir():
    """Test finding environment.yml in parent directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create environment.yml in root
        env_file = tmpdir / "environment.yml"
        env_file.write_text("name: test-env\n")

        # Create subdirectory
        subdir = tmpdir / "subdir"
        subdir.mkdir()

        # Should find the file from subdirectory
        result = find_environment_file(str(subdir))
        assert result == env_file


def test_find_environment_file_not_found():
    """Test when environment.yml is not found."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = find_environment_file(tmpdir)
        assert result is None


def test_parse_environment_file():
    """Test parsing valid environment.yml file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yml"
        env_content = """
name: test-env
dependencies:
  - python=3.9
  - numpy
channels:
  - conda-forge
"""
        env_file.write_text(env_content)

        result = parse_environment_file(env_file)
        assert result["name"] == "test-env"
        assert "dependencies" in result
        assert "channels" in result


def test_parse_environment_file_not_found():
    """Test parsing non-existent file."""
    with pytest.raises(FileNotFoundError):
        parse_environment_file(Path("/nonexistent/file.yml"))


def test_get_environment_name():
    """Test extracting environment name from parsed data."""
    env_data = {"name": "my-env", "dependencies": ["python=3.9"]}

    result = get_environment_name(env_data)
    assert result == "my-env"


def test_get_environment_name_missing():
    """Test extracting environment name when not present."""
    env_data = {"dependencies": ["python=3.9"]}

    result = get_environment_name(env_data)
    assert result is None


def test_get_conda_environment_name_success():
    """Test successful extraction of environment name."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yml"
        env_file.write_text("name: integration-test-env\n")

        result = get_conda_environment_name(tmpdir)
        assert result == "integration-test-env"


def test_get_conda_environment_name_no_file():
    """Test when no environment.yml file exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = get_conda_environment_name(tmpdir)
        assert result is None


def test_get_conda_environment_name_invalid_yaml():
    """Test when environment.yml contains invalid YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yml"
        env_file.write_text("invalid: yaml: content: [[[")

        result = get_conda_environment_name(tmpdir)
        assert result is None
