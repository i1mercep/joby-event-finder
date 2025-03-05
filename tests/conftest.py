import json
from typing import Any


def load_fixture(file_name: str) -> dict[str, Any]:
    if file_name is None:
        return {}
    with open(file_name, encoding="utf-8") as file:
        return json.load(file)


def clean_sql_str(sql: str) -> str:
    """Remove newlines and trim extra whitespaces from SQL string."""
    return " ".join(sql.replace("\n", " ").split())
