from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
