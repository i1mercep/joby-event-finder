from pydantic import ConfigDict
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel

from src.utils import pascal_to_snake_case


class Base(SQLModel):
    """Base class for declarative models."""

    __abstract__ = True

    model_config = ConfigDict(validate_assignment=True, from_attributes=True)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: PLW3201, N805
        """Generate __tablename__ automatically as pascalCase."""
        return pascal_to_snake_case(cls.__name__)


class Distance(SQLModel):
    """A distance between two points."""

    distance_km: float
