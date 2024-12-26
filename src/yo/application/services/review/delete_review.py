from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from yo.application.exceptions import ReviewNotFoundError
from yo.application.postgres.orm_models import Review

from yo.application.postgres import get_postgres_async_conn


class DeleteReviewProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, review_id: UUID, user_id: UUID) -> None:
        review = await self._db_conn.get(Review, review_id)

        if not review:
            raise ReviewNotFoundError(message="There is no such review")

        if review.user_id != user_id:
            raise ReviewNotFoundError(
                message="You don't have permission to delete this review",
            )

        await self._db_conn.delete(review)
        await self._db_conn.commit()

        return None


def get_delete_review_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> DeleteReviewProcessor:
    return DeleteReviewProcessor(db_conn=db_conn)
