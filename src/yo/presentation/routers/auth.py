from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Cookie, Form, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from yo.application import (
    get_postgres_async_conn,
    AsyncSessionManager,
    get_session_manager,
    UserLoginProcessor,
    get_user_login_processor,
    AdminLoginProcessor,
    get_admin_login_processor,
    CreateUserProcessor,
    get_create_user_processor,
    User,
    UserNotFoundError,
    UserType,
)
from yo.presentation.pydantic_forms import UserForm


def _get_login_templates():
    return Jinja2Templates(directory="presentation/templates/login")


def _get_register_templates():
    return Jinja2Templates(directory="presentation/templates/register")


auth_router = APIRouter()


@auth_router.get("/login/user")  # type: ignore
async def get_user_login(
    request: Request,
    login_templates: Jinja2Templates = Depends(_get_login_templates),
):
    return login_templates.TemplateResponse(
        "user_login.html", {"request": request}
    )


@auth_router.post("/login/user")  # type: ignore
async def login(
    form_data: UserForm = Form(...),
    processor: UserLoginProcessor = Depends(get_user_login_processor),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> JSONResponse:
    user_id = await processor.process(
        username=form_data.username, password=form_data.password
    )

    response = JSONResponse(
        content={
            "message": "Login successful",
            "username": form_data.username,
        }
    )

    session_id = await session_manager.create_session(user_id)

    response.set_cookie("session_id", session_id)

    return response


@auth_router.get("/login/admin")  # type: ignore
async def get_login_form(
    request: Request,
    login_templates: Jinja2Templates = Depends(_get_login_templates),
):
    return login_templates.TemplateResponse(
        "admin_login.html", {"request": request}
    )


@auth_router.post("/login/admin")  # type: ignore
async def login(
    form_data: UserForm = Form(...),
    processor: AdminLoginProcessor = Depends(get_admin_login_processor),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> JSONResponse:
    admin_id = await processor.process(
        username=form_data.username, password=form_data.password
    )

    response = JSONResponse(
        content={
            "message": "Login successful",
            "username": form_data.username,
        }
    )

    session_id = await session_manager.create_session(admin_id, UserType.ADMIN)

    response.set_cookie("session_id", session_id)

    return response


@auth_router.get("/register/user")  # type: ignore
async def get_user_register(
    request: Request,
    register_templates: Jinja2Templates = Depends(_get_register_templates),
):
    return register_templates.TemplateResponse(
        "user_register.html", {"request": request}
    )


@auth_router.post("/register/user")  # type: ignore
async def register(
    form_data: UserForm = Form(...),
    processor: CreateUserProcessor = Depends(get_create_user_processor),
) -> dict:
    await processor.process(
        username=form_data.username, password=form_data.password
    )

    return {
        "message": "User created successfully",
        "username": form_data.username,
    }


@auth_router.get("/get-user-sessionid")  # type: ignore
async def get_user_info(
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> dict:
    """
    штука для отладки
    """
    user_id = await session_manager.get_id(session_id)

    user = await db_conn.get(User, user_id)

    if not user:
        raise UserNotFoundError(message="User not found")

    return {"user_id": user.id, "username": user.username}
