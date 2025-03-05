import pkgutil
import re
from importlib import import_module

from fastapi import APIRouter

EXCLUIDED_MODULES = ["__init__"]


def load_routers(endpoints_path: str) -> dict[str, APIRouter]:
    """Load the endpoint routes to the dictionary."""
    routers_by_name: dict[str, APIRouter] = {}
    package_name = endpoints_path.replace("/", ".")
    package = import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name in EXCLUIDED_MODULES:
            continue
        module = import_module(f"{package_name}.{module_name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            routers_by_name[module_name] = router
    return routers_by_name


def pascal_to_snake_case(name: str) -> str:
    """Convert PascalCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
