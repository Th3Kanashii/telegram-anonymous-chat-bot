from datetime import datetime, timezone
from typing import Annotated, TypeAlias

from sqlalchemy import BigInteger, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry


Int16: TypeAlias = Annotated[int, 16]
Int64: TypeAlias = Annotated[int, 64]


class Base(DeclarativeBase):
    """
    Base class for all models.
    """

    registry = registry(
        type_annotation_map={Int16: Integer, Int64: BigInteger, datetime: DateTime(timezone=True)},
    )


class TimestampMixin:
    """
    Mixin class for models that require a created_at and updated_at column.
    """

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=func.now(),
        server_default=func.now(),
    )
