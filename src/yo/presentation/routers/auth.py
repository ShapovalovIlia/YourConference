from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Cookie, Form
from fastapi.responses import JSONResponse

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
)
from yo.presentation.pydantic_forms import UserForm


auth_router = APIRouter()


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

    session_id = await session_manager.create_session(admin_id)

    response.set_cookie("session_id", session_id)

    return response


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


@auth_router.get("/test-session") # type: ignore
async def get_user_info(
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)

    user = await db_conn.get(User, user_id)

    if not user:
        raise UserNotFoundError(message="User not found")

    return {"user_id": user.id, "username": user.username}
