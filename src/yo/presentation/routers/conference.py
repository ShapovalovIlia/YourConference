from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates

from yo.application import (
    get_get_conferences_processor,
    GetConferencesProcessor,
)


conference_router = APIRouter(prefix="/conferences")


def _get_conferences_templates() -> Jinja2Templates:
    return Jinja2Templates(directory="presentation/templates/conferences")


@conference_router.get("")  # type: ignore
async def get_conferences_list(
    request: Request,  # добавляем зависимость request
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    processor: GetConferencesProcessor = Depends(
        get_get_conferences_processor
    ),
    templates: Jinja2Templates = Depends(_get_conferences_templates),
):
    conferences = await processor.process(skip=skip, limit=limit)

    return templates.TemplateResponse(
        "conferences_list.html",
        {
            "request": request,
            "conferences": conferences,
            "skip": skip,
            "limit": limit,
        },
    )
