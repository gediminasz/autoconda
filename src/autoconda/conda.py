"""Conda interaction utilities for autoconda."""

import subprocess


class CondaError(Exception):
    """Exception raised when conda operations fail."""

    pass


def run_in_environment(env_name: str, command: list[str]) -> int:
    """Run a command in a specific conda environment.

    Args:
        env_name: Name of the environment to run the command in.
        command: Command and arguments to run.

    Returns:
        Exit code of the command.

    Raises:
        CondaError: If the command fails to execute.
    """
    # Use conda run to execute the command in the environment
    # --no-capture-output ensures proper handling of stdin/stdout/stderr
    conda_command = ["conda", "run", "-n", env_name, "--no-capture-output"] + command

    try:
        result = subprocess.run(conda_command)
        return result.returncode
    except subprocess.SubprocessError as e:
        raise CondaError(f"Failed to run command in environment '{env_name}': {e}") from e
