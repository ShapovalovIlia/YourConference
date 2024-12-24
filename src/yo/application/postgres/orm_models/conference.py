from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class ConferencesOrm(Base):
    __tablename__ = "conferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    topic: Mapped[str] = mapped_column(nullable=False)
    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id", ondelete="SET NULL")
    )
    start_date: Mapped[date] = mapped_column(nullable=False)
    end_date: Mapped[date] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    cond_participation: Mapped[str] = mapped_column(nullable=False)
