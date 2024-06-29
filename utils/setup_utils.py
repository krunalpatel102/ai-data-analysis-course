import sys
from pathlib import Path
import importlib
import pkgutil
import pandas as pd

def find_project_root(start_path: Path, target_file: str) -> Path:
    """Recursively search for the project root directory containing the target file starting from the given path."""
    current_path = start_path
    while current_path != current_path.parent:
        if (current_path / target_file).exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(f"{target_file} not found in any parent directories.")

# Determine the project root starting from the current working directory
current_dir = Path.cwd()
project_root = find_project_root(current_dir, 'environment.yml')

# Add the project root to the system path
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import all modules in the utils package
utils_dir = project_root / 'utils'
for _, module_name, _ in pkgutil.iter_modules([str(utils_dir)]):
    module = importlib.import_module(f"utils.{module_name}")
    globals()[module_name] = module
