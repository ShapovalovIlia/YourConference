from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class TopicsOrm(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
