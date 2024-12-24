from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends

from yo.application.exceptions import ReviewAlreadyExistsError
from yo.application.postgres.orm_models import Review

from yo.application.postgres import get_postgres_async_conn


class CreateReviewProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(
        self, *, conference_id: int, user_id: int, rating: int, text: str
    ) -> None:
        review = Review(
            conference_id=conference_id,
            user_id=user_id,
            rating=rating,
            text=text,
        )

        try:
            self._db_conn.add(review)
            await self._db_conn.commit()

        except IntegrityError:  # TODO: более узко ловить ошибку
            raise ReviewAlreadyExistsError(
                message="The user has already left a review for this conference.",
            )

        return None


def get_create_review_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> CreateReviewProcessor:
    return CreateReviewProcessor(db_conn=db_conn)
