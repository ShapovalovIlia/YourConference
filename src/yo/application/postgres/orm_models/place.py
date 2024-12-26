from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Place(Base):
    __tablename__ = "places"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
