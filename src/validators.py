import re
from datetime import UTC, datetime


def validate_username(v: str) -> str:
    if not re.match(r"^[a-zA-Z0-9_]+$", v):
        raise ValueError("Username must be alphanumeric, underscores are allowed")
    max_length = 20
    min_length = 3
    if len(v) < min_length or len(v) > max_length:
        raise ValueError("Username must be between 3 and 20 characters")
    if " " in v:
        raise ValueError("Username cannot contain any whitespace")
    return v.lower()


def validate_email(v: str) -> str:
    v = v.strip()
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, v):
        raise ValueError("Invalid email address")
    return v.lower()


def validate_non_naive(v: datetime) -> datetime:
    """Validate that the timestamp is not naive"""
    if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
        raise ValueError("Timestamp must be timezone aware")
    return v


def convert_naive_to_utc(v: datetime) -> datetime:
    """Convert naive timestamp to UTC."""
    if v.tzinfo is None:
        v = v.replace(tzinfo=UTC)
    return v.astimezone(UTC)
