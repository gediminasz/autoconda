import argparse
import os
import subprocess
import sys

from . import __version__
from .environment import get_conda_environment_name

parser = argparse.ArgumentParser(description=f"autoconda {__version__}")
parser.add_argument(
    "--path",
    "-p",
    help="Path to start searching for environment.yml (defaults to current directory)",
    default=os.getcwd(),
)
parser.add_argument("command", nargs="+", help="Command and arguments to run")


def main(path: str, command: list[str]):
    env_name = get_conda_environment_name(path)

    if env_name is None:
        print(
            "Error: No environment.yml file found or no environment name specified in the file.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = subprocess.run(["conda", "run", "-n", env_name, "--no-capture-output", *command])
    sys.exit(result.returncode)


if __name__ == "__main__":
    args = parser.parse_args()
    main(**vars(args))
