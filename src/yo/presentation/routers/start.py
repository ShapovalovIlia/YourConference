from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="presentation/templates")

start_router = APIRouter()


@start_router.get("/", response_class=HTMLResponse)  # type: ignore
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
