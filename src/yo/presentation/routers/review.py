from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, HTTPException, Depends, Cookie, Query, Form

from yo.application import (
    get_postgres_async_conn,
    AsyncSessionManager,
    Review,
    get_session_manager,
    CreateReviewProcessor,
    get_create_review_processor,
)

from yo.presentation.validation_models import ReviewForm

review_router = APIRouter(prefix="/reviews")


@review_router.post("")  # type: ignore
async def create_review(
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    processor: CreateReviewProcessor = Depends(get_create_review_processor),
    session_id: str = Cookie(...),
    conference_id: int = Query(...),
    review_form: ReviewForm = Form(),
):
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    await processor.process(
        conference_id=conference_id,
        user_id=user_id,
        rating=review_form.rating,
        text=review_form.text,
    )

    return {"message": "review created"}


@review_router.delete("/{review_id}")  # type: ignore
async def delete_review(
    review_id: int,
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    review = await db_conn.get(Review, review_id)

    if not review:
        raise HTTPException(status_code=400, detail="There is no such review")

    if review.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this review",
        )

    await db_conn.delete(review)
    await db_conn.commit()

    return {"message": "review deleted"}
