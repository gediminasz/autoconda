import argparse
import os
import subprocess
import sys
from pathlib import Path

from . import __version__
from .environment import get_conda_environment_name

parser = argparse.ArgumentParser(prog="autoconda")
parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
parser.add_argument(
    "--path",
    "-p",
    help="path to start searching for environment.yml or environment.yaml (defaults to current directory)",
    default=os.getcwd(),
    type=Path,
)
parser.add_argument("command", nargs="+", help="Command and arguments to run")


def autoconda(path: Path, command: list[str]):
    env_name = get_conda_environment_name(path)

    if env_name is None:
        print(
            "Error: No environment.yml or environment.yaml file found or no environment name specified in the file.",
            file=sys.stderr,
        )
        sys.exit(1)

    result = subprocess.run(["conda", "run", "-n", env_name, "--no-capture-output", *command])
    sys.exit(result.returncode)


def main():
    args = parser.parse_args()
    autoconda(**vars(args))


if __name__ == "__main__":
    main()
