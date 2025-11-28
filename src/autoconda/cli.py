"""Command-line interface for autoconda."""

import argparse
import os
import sys

from .conda import CondaError, run_in_environment
from .environment import get_conda_environment_name


def cmd_run(command: list[str], path: str):
    try:
        env_name = get_conda_environment_name(path)

        if env_name is None:
            print(
                "Error: No environment.yml file found or no environment name specified in the file.",
                file=sys.stderr,
            )
            sys.exit(1)

        print(f"Running command in conda environment '{env_name}': {' '.join(command)}")
        exit_code = run_in_environment(env_name, command)
        sys.exit(exit_code)

    except CondaError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Autoconda - Automatic conda environment management.

    A CLI tool that automatically parses conda environment name from environment.yml
    and runs commands within it.
    """
    # Check for 'run' subcommand and handle it specially
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # Remove 'run' from argv to make it work like the direct command
        sys.argv.pop(1)

    parser = argparse.ArgumentParser(
        description="Autoconda - Automatic conda environment management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  autoconda python script.py
  autoconda python -c "import numpy; print(numpy.__version__)"
  autoconda jupyter notebook
  autoconda -- python --version

  autoconda run python script.py  # 'run' subcommand also works""",
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument(
        "--path",
        "-p",
        help="Path to start searching for environment.yml (defaults to current directory)",
        default=os.getcwd(),
    )
    parser.add_argument("command", nargs="*", help="Command and arguments to run")

    args = parser.parse_args()

    if args.version:
        from . import __version__

        print(f"autoconda {__version__}")
        sys.exit(0)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmd_run(args.command, args.path)


if __name__ == "__main__":
    main()
