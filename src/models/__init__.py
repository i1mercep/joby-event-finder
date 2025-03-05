"""Import all modules in the current directory. Needed for migrations script."""

import importlib
import os
import pkgutil

# Get the directory of the current file
current_dir = os.path.dirname(__file__)

excluded_modules = ["__init__"]

# Iterate through all (except excluded) modules in the current directory and import them
for _, module_name, _ in pkgutil.iter_modules([current_dir]):
    if module_name not in excluded_modules:
        importlib.import_module(f".{module_name}", package=__name__)
