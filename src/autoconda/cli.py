"""Command-line interface for autoconda."""

import sys
import argparse
from pathlib import Path
from typing import Optional, List

from .environment import get_conda_environment_name
from .conda import CondaError, activate_environment, run_in_environment


def cmd_activate(args):
    """Activate the conda environment specified in environment.yml.
    
    This command finds the environment.yml file starting from the current directory
    (or specified path) and walking up the directory tree, then activates the
    environment specified in that file.
    """
    try:
        env_name = get_conda_environment_name(args.path)
        
        if env_name is None:
            print("Error: No environment.yml file found or no environment name specified in the file.",
                  file=sys.stderr)
            sys.exit(1)
        
        print(f"Activating conda environment: {env_name}")
        activate_environment(env_name)
        
    except CondaError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_run(args):
    """Run a command in the conda environment specified in environment.yml.
    
    This command finds the environment.yml file starting from the current directory
    (or specified path) and walking up the directory tree, then runs the specified
    command in that environment.
    """
    command = args.command
    
    if not command:
        print("Error: No command specified.", file=sys.stderr)
        sys.exit(2)
    
    try:
        env_name = get_conda_environment_name(args.path)
        
        if env_name is None:
            print("Error: No environment.yml file found or no environment name specified in the file.",
                  file=sys.stderr)
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


def cmd_info(args):
    """Show information about the detected environment.
    
    This command finds and displays information about the conda environment
    specified in environment.yml without activating it or running any commands.
    """
    try:
        from .environment import find_environment_file, parse_environment_file
        
        env_file = find_environment_file(args.path)
        
        if env_file is None:
            print("No environment.yml file found.")
            sys.exit(1)
        
        print(f"Environment file: {env_file}")
        
        try:
            env_data = parse_environment_file(env_file)
            env_name = env_data.get('name')
            
            if env_name:
                print(f"Environment name: {env_name}")
                
                # Show additional info if available
                if 'dependencies' in env_data:
                    dep_count = len(env_data['dependencies'])
                    print(f"Dependencies: {dep_count} items")
                
                if 'channels' in env_data:
                    channels = env_data['channels']
                    print(f"Channels: {', '.join(channels)}")
            else:
                print("No environment name specified in environment.yml")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error parsing environment.yml: {e}", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Autoconda - Automatic conda environment management.
    
    A CLI tool that automatically parses conda environment name from environment.yml
    and provides commands to activate the environment or run commands within it.
    """
    parser = argparse.ArgumentParser(
        description="Autoconda - Automatic conda environment management",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='store_true', help='Show version and exit')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Activate command
    activate_parser = subparsers.add_parser(
        'activate',
        help='Activate the conda environment specified in environment.yml'
    )
    activate_parser.add_argument(
        '--path', '-p',
        help='Path to start searching for environment.yml (defaults to current directory)'
    )
    activate_parser.set_defaults(func=cmd_activate)
    
    # Run command
    run_parser = subparsers.add_parser(
        'run',
        help='Run a command in the conda environment specified in environment.yml',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  autoconda run python script.py
  autoconda run -- python -c "import numpy; print(numpy.__version__)"
  autoconda run jupyter notebook
  autoconda run -- python --version"""
    )
    run_parser.add_argument(
        '--path', '-p',
        help='Path to start searching for environment.yml (defaults to current directory)'
    )
    run_parser.add_argument(
        'command',
        nargs=argparse.REMAINDER,
        help='Command and arguments to run'
    )
    run_parser.set_defaults(func=cmd_run)
    
    # Info command
    info_parser = subparsers.add_parser(
        'info',
        help='Show information about the detected environment'
    )
    info_parser.add_argument(
        '--path', '-p',
        help='Path to start searching for environment.yml (defaults to current directory)'
    )
    info_parser.set_defaults(func=cmd_info)
    
    args = parser.parse_args()
    
    if args.version:
        from . import __version__
        print(f"autoconda {__version__}")
        sys.exit(0)
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    # Call the appropriate command function
    args.func(args)


if __name__ == '__main__':
    main()