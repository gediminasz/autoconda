import tempfile
from pathlib import Path

from autoconda.environment import find_environment_file, get_conda_environment_name


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


def test_find_environment_yaml_file():
    """Test finding environment.yaml in current directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create environment.yaml in temp directory
        env_file = Path(tmpdir) / "environment.yaml"
        env_file.write_text("name: test-env\n")

        # Should find the file
        result = find_environment_file(tmpdir)
        assert result == env_file


def test_get_conda_environment_name_from_yaml():
    """Test successful extraction of environment name from .yaml file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "environment.yaml"
        env_file.write_text("name: yaml-test-env\n")

        result = get_conda_environment_name(tmpdir)
        assert result == "yaml-test-env"


def test_yml_preferred_over_yaml():
    """Test that .yml is preferred over .yaml when both exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create both files
        yml_file = Path(tmpdir) / "environment.yml"
        yml_file.write_text("name: yml-env\n")
        
        yaml_file = Path(tmpdir) / "environment.yaml"
        yaml_file.write_text("name: yaml-env\n")

        # Should find .yml file first
        result = find_environment_file(tmpdir)
        assert result == yml_file
        
        # Should extract name from .yml file
        env_name = get_conda_environment_name(tmpdir)
        assert env_name == "yml-env"
