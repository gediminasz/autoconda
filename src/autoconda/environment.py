from pathlib import Path

import yaml


def find_environment_file(start_path: str) -> Path | None:
    current_path = Path(start_path).resolve()

    while True:
        for ext in ["yml", "yaml"]:
            env_file = current_path / f"environment.{ext}"
            if env_file.exists():
                return env_file
        if current_path == current_path.parent:
            return None
        current_path = current_path.parent


def get_conda_environment_name(start_path: str) -> str | None:
    env_file = find_environment_file(start_path)
    if env_file is None:
        return None

    try:
        with open(env_file) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError:
        return None

    return data.get("name")
