"""Command-line interface for autoconda."""

import sys
import click
from pathlib import Path
from typing import Optional

from .environment import get_conda_environment_name
from .conda import CondaError, activate_environment, run_in_environment


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version and exit')
@click.pass_context
def main(ctx, version):
    """Autoconda - Automatic conda environment management.
    
    A CLI tool that automatically parses conda environment name from environment.yml
    and provides commands to activate the environment or run commands within it.
    """
    if version:
        from . import __version__
        click.echo(f"autoconda {__version__}")
        sys.exit(0)
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help='Path to start searching for environment.yml (defaults to current directory)')
def activate(path: Optional[str]):
    """Activate the conda environment specified in environment.yml.
    
    This command finds the environment.yml file starting from the current directory
    (or specified path) and walking up the directory tree, then activates the
    environment specified in that file.
    """
    try:
        env_name = get_conda_environment_name(path)
        
        if env_name is None:
            click.echo("Error: No environment.yml file found or no environment name specified in the file.",
                      err=True)
            sys.exit(1)
        
        click.echo(f"Activating conda environment: {env_name}")
        activate_environment(env_name)
        
    except CondaError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@main.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help='Path to start searching for environment.yml (defaults to current directory)')
@click.pass_context
def run(ctx, path: Optional[str]):
    """Run a command in the conda environment specified in environment.yml.
    
    This command finds the environment.yml file starting from the current directory
    (or specified path) and walking up the directory tree, then runs the specified
    command in that environment.
    
    Examples:
        autoconda run python script.py
        autoconda run -- python -c "import numpy; print(numpy.__version__)"
        autoconda run jupyter notebook
        autoconda run -- python --version
    """
    command = ctx.args
    
    if not command:
        click.echo("Error: No command specified.", err=True)
        click.echo(ctx.get_help())
        sys.exit(2)
    try:
        env_name = get_conda_environment_name(path)
        
        if env_name is None:
            click.echo("Error: No environment.yml file found or no environment name specified in the file.",
                      err=True)
            sys.exit(1)
        
        click.echo(f"Running command in conda environment '{env_name}': {' '.join(command)}")
        exit_code = run_in_environment(env_name, command)
        sys.exit(exit_code)
        
    except CondaError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--path', '-p', type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help='Path to start searching for environment.yml (defaults to current directory)')
def info(path: Optional[str]):
    """Show information about the detected environment.
    
    This command finds and displays information about the conda environment
    specified in environment.yml without activating it or running any commands.
    """
    try:
        from .environment import find_environment_file, parse_environment_file
        
        env_file = find_environment_file(path)
        
        if env_file is None:
            click.echo("No environment.yml file found.")
            sys.exit(1)
        
        click.echo(f"Environment file: {env_file}")
        
        try:
            env_data = parse_environment_file(env_file)
            env_name = env_data.get('name')
            
            if env_name:
                click.echo(f"Environment name: {env_name}")
                
                # Show additional info if available
                if 'dependencies' in env_data:
                    dep_count = len(env_data['dependencies'])
                    click.echo(f"Dependencies: {dep_count} items")
                
                if 'channels' in env_data:
                    channels = env_data['channels']
                    click.echo(f"Channels: {', '.join(channels)}")
            else:
                click.echo("No environment name specified in environment.yml")
                sys.exit(1)
                
        except Exception as e:
            click.echo(f"Error parsing environment.yml: {e}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()