from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from yo.application.exceptions import ReviewAlreadyExistsError
from yo.application.postgres.orm_models import Review
from yo.application.postgres import get_postgres_async_conn


class CreateReviewProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(
        self, *, conference_id: UUID, user_id: UUID, rating: int, text: str
    ) -> None:
        if await self._check_review_exists(
            user_id=user_id, conference_id=conference_id
        ):
            raise ReviewAlreadyExistsError(
                message="The user has already left a review for this conference.",
            )

        review = Review(
            conference_id=conference_id,
            user_id=user_id,
            rating=rating,
            text=text,
        )

        self._db_conn.add(review)
        await self._db_conn.commit()

    async def _check_review_exists(
        self, user_id: UUID, conference_id: UUID
    ) -> bool:
        query = select(Review).where(
            Review.user_id == user_id, Review.conference_id == conference_id
        )
        check = await self._db_conn.execute(query)

        return len(check.all()) > 0


def get_create_review_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> CreateReviewProcessor:
    return CreateReviewProcessor(db_conn=db_conn)
