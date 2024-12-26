from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
