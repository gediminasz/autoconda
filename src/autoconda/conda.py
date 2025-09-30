"""Conda interaction utilities for autoconda."""

import os
import subprocess


class CondaError(Exception):
    """Exception raised when conda operations fail."""

    pass


def check_conda_available() -> bool:
    """Check if conda is available in the system.

    Returns:
        True if conda is available, False otherwise.
    """
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_conda_environments() -> list[str]:
    """Get list of available conda environments.

    Returns:
        List of environment names.

    Raises:
        CondaError: If conda is not available or command fails.
    """
    if not check_conda_available():
        raise CondaError("Conda is not available in the system")

    try:
        result = subprocess.run(
            ["conda", "env", "list", "--json"], capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            raise CondaError(f"Failed to list conda environments: {result.stderr}")

        import json

        env_data = json.loads(result.stdout)

        # Extract environment names from paths
        environments = []
        for env_path in env_data.get("envs", []):
            env_name = os.path.basename(env_path)
            if env_name != "envs":  # Skip the base envs directory
                environments.append(env_name)

        return environments
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        raise CondaError(f"Failed to parse conda environments: {e}") from e


def environment_exists(env_name: str) -> bool:
    """Check if a conda environment exists.

    Args:
        env_name: Name of the environment to check.

    Returns:
        True if environment exists, False otherwise.
    """
    try:
        environments = get_conda_environments()
        return env_name in environments
    except CondaError:
        return False


def activate_environment(env_name: str) -> None:
    """Activate a conda environment by spawning an interactive shell.

    Similar to 'poetry shell', this spawns a new shell with the conda environment
    activated using 'conda run'.

    Args:
        env_name: Name of the environment to activate.

    Raises:
        CondaError: If conda is not available or environment doesn't exist.
    """
    if not check_conda_available():
        raise CondaError("Conda is not available in the system")

    if not environment_exists(env_name):
        raise CondaError(f"Environment '{env_name}' does not exist")

    # Determine the shell to use
    shell = os.environ.get("SHELL", "/bin/bash")
    shell_name = os.path.basename(shell)

    # Use conda run to spawn an interactive shell in the environment
    # --no-capture-output ensures interactive shell works properly
    conda_command = ["conda", "run", "--name", env_name, "--no-capture-output", shell_name]

    try:
        subprocess.run(conda_command)
    except subprocess.SubprocessError as e:
        raise CondaError(f"Failed to activate environment '{env_name}': {e}") from e


def run_in_environment(env_name: str, command: list[str]) -> int:
    """Run a command in a specific conda environment.

    Args:
        env_name: Name of the environment to run the command in.
        command: Command and arguments to run.

    Returns:
        Exit code of the command.

    Raises:
        CondaError: If conda is not available or environment doesn't exist.
    """
    if not check_conda_available():
        raise CondaError("Conda is not available in the system")

    if not environment_exists(env_name):
        raise CondaError(f"Environment '{env_name}' does not exist")

    # Use conda run to execute the command in the environment
    conda_command = ["conda", "run", "-n", env_name] + command

    try:
        result = subprocess.run(conda_command)
        return result.returncode
    except subprocess.SubprocessError as e:
        raise CondaError(f"Failed to run command in environment '{env_name}': {e}") from e
