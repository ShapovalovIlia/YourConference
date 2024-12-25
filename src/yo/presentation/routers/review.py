from fastapi import APIRouter, Depends, Cookie, Query, Form

from yo.application import (
    AsyncSessionManager,
    get_session_manager,
    CreateReviewProcessor,
    get_create_review_processor,
    DeleteReviewProcessor,
    get_delete_review_processor,
)

from yo.presentation.pydantic_forms import ReviewForm

review_router = APIRouter(prefix="/reviews")


@review_router.post("")  # type: ignore
async def create_review(
    session_id: str = Cookie(...),
    conference_id: int = Query(...),
    review_form: ReviewForm = Form(),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    processor: CreateReviewProcessor = Depends(get_create_review_processor),
):
    user_id = await session_manager.get_user_id(session_id)

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
    session_id: str = Cookie(...),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    proccessor: DeleteReviewProcessor = Depends(get_delete_review_processor),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)

    await proccessor.process(review_id=review_id, user_id=user_id)

    return {"message": "review deleted"}
