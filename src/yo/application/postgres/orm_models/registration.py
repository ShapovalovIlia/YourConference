from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Registration(Base):
    __tablename__ = "registrations"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    conference_id: Mapped[UUID] = mapped_column(
        ForeignKey("conferences.id", ondelete="CASCADE"),
    )
    recommended: Mapped[bool] = mapped_column(default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "conference_id",
        ),
    )
