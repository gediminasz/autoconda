# Autoconda

A Python CLI tool for automatic conda environment management, inspired by `poetry run`.

## Overview

Autoconda automatically parses the conda environment name from `environment.yml` files and provides convenient commands to:

1. **Activate environments** - analogous to `conda activate`
2. **Run commands in environments** - analogous to `conda run`

The tool automatically searches for `environment.yml` files starting from the current directory and walking up the directory tree, making it convenient to use from anywhere within your project.

## Installation

```bash
pip install autoconda
```

Or install from source:

```bash
git clone https://github.com/gediminasz/autoconda.git
cd autoconda
pip install -e .
```

## Usage

### Activate Environment

Activate the conda environment specified in `environment.yml`:

```bash
autoconda activate
```

You can also specify a custom path to search for the environment file:

```bash
autoconda activate --path /path/to/project
```

### Run Commands

Run a command in the conda environment specified in `environment.yml`:

```bash
autoconda run python script.py
autoconda run python -c "import numpy; print(numpy.__version__)"
autoconda run jupyter notebook
```

### Environment Information

Show information about the detected environment without activating it:

```bash
autoconda info
```

### Help

Get help for any command:

```bash
autoconda --help
autoconda activate --help
autoconda run --help
```

## Environment File Format

Autoconda expects a standard conda `environment.yml` file with at least a `name` field:

```yaml
name: my-project-env
dependencies:
  - python=3.9
  - numpy
  - pandas
  - pip
  - pip:
    - requests
channels:
  - conda-forge
  - defaults
```

## Examples

1. **Simple activation**:
   ```bash
   # In a directory with environment.yml
   autoconda activate
   ```

2. **Run Python script**:
   ```bash
   autoconda run python train_model.py
   ```

3. **Start Jupyter notebook**:
   ```bash
   autoconda run jupyter notebook
   ```

4. **Check environment info**:
   ```bash
   autoconda info
   ```

## Requirements

- Python 3.7+
- Conda or Miniconda installed and available in PATH
- An `environment.yml` file with a `name` field

## License

MIT License - see [LICENSE](LICENSE) file for details.