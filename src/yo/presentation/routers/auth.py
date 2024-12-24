from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, Cookie
from fastapi.responses import JSONResponse

from yo.infrastructure import (
    get_postgres_async_conn,
    UsersOrm,
    AdminsOrm,
    AsyncSessionManager,
    get_session_manager,
)
from yo.presentation.validation_models import UserForm


auth_router = APIRouter()


@auth_router.post("/login/user")  # type: ignore
async def login(
    form_data: UserForm = Depends(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> JSONResponse:
    query = select(UsersOrm).filter(UsersOrm.username == form_data.username)
    result = await db_conn.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    if form_data.password != user.password:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    session_id = await session_manager.create_session(user.id)

    response = JSONResponse(
        content={"message": "Login successful", "username": user.username}
    )

    response.set_cookie("session_id", session_id)

    return response


@auth_router.post("/login/admin")  # type: ignore
async def login(
    form_data: UserForm = Depends(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> JSONResponse:
    query = select(AdminsOrm).where(AdminsOrm.username == form_data.username)
    result = await db_conn.execute(query)
    admin = result.scalar_one_or_none()

    if admin is None:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    if form_data.password != admin.password:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    session_id = await session_manager.create_session(admin.id)

    response = JSONResponse(
        content={"message": "Login successful", "username": admin.username}
    )

    response.set_cookie("session_id", session_id)

    return response


@auth_router.get("/test-session") # type: ignore
async def get_user_info(
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    user = await db_conn.get(UsersOrm, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"user_id": user.id, "username": user.username}


@auth_router.post("/register/user")  # type: ignore
async def register(
    form_data: UserForm = Depends(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    new_user = UsersOrm(
        username=form_data.username, password=form_data.password
    )

    try:
        db_conn.add(new_user)
        await db_conn.commit()
        await db_conn.refresh(new_user)

    except IntegrityError:
        await db_conn.rollback()

        raise HTTPException(
            status_code=409, detail="User with such username already exists"
        )

    return {
        "message": "User created successfully",
        "username": new_user.username,
    }
