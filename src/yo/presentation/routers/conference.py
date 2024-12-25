from fastapi import APIRouter, Depends, Query

from yo.application import (
    get_get_conferences_processor,
    GetConferencesProcessor,
)


conference_router = APIRouter(prefix="/conferences")


@conference_router.get("")  # type: ignore
async def get_conferences_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    processor: GetConferencesProcessor = Depends(
        get_get_conferences_processor
    ),
):
    conferences = await processor.process(skip=skip, limit=limit)

    return conferences
