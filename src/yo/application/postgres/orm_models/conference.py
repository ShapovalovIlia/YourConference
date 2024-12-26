from datetime import date
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Conference(Base):
    __tablename__ = "conferences"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    topic: Mapped[str] = mapped_column(nullable=False)
    place_id: Mapped[UUID] = mapped_column(
        ForeignKey("places.id", ondelete="SET NULL"),
    )
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    cond_participation: Mapped[str] = mapped_column(nullable=False)
