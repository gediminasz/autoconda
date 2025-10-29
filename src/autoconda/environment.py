"""Environment parsing utilities for autoconda."""

import os
from pathlib import Path
from typing import Any

import yaml


def find_environment_file(start_path: str | None = None) -> Path | None:
    """Find environment.yml file starting from the given path and walking up the directory tree.

    Args:
        start_path: Starting directory to search from. Defaults to current directory.

    Returns:
        Path to environment.yml file if found, None otherwise.
    """
    if start_path is None:
        start_path = os.getcwd()

    current_path = Path(start_path).resolve()

    while current_path != current_path.parent:
        env_file = current_path / "environment.yml"
        if env_file.exists():
            return env_file
        current_path = current_path.parent

    # Check root directory
    env_file = current_path / "environment.yml"
    if env_file.exists():
        return env_file

    return None


def parse_environment_file(env_file_path: Path) -> dict[str, Any]:
    """Parse environment.yml file and return its contents.

    Args:
        env_file_path: Path to the environment.yml file.

    Returns:
        Parsed YAML content as dictionary.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        yaml.YAMLError: If the file contains invalid YAML.
    """
    if not env_file_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_file_path}")

    with open(env_file_path) as f:
        data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}


def get_environment_name(env_data: dict[str, Any]) -> str | None:
    """Extract environment name from parsed environment.yml data.

    Args:
        env_data: Parsed environment.yml content.

    Returns:
        Environment name if found, None otherwise.
    """
    return env_data.get("name")


def get_conda_environment_name(start_path: str | None = None) -> str | None:
    """Get conda environment name from environment.yml file.

    This is the main function that combines all the parsing logic.

    Args:
        start_path: Starting directory to search from. Defaults to current directory.

    Returns:
        Environment name if found and valid, None otherwise.
    """
    env_file = find_environment_file(start_path)
    if env_file is None:
        return None

    try:
        env_data = parse_environment_file(env_file)
        return get_environment_name(env_data)
    except (yaml.YAMLError, FileNotFoundError):
        return None
