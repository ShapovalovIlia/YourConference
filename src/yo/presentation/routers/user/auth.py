from uuid import uuid4

import redis.asyncio as aioredis # type: ignore

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, Cookie
from fastapi.responses import JSONResponse

from yo.infrastructure.di import get_postgres_async_conn, get_redis_async_conn
from yo.infrastructure.postgres.orm_models import UsersOrm
from yo.presentation.validation_models import UserForm


auth_router = APIRouter(prefix="")


@auth_router.post("/login") # type: ignore
async def login(
    form_data: UserForm = Depends(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    redis: aioredis.Redis = Depends(get_redis_async_conn),
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

    session_id = str(uuid4())
    await redis.set(session_id, user.id, ex=30)  # TODO поменять после тестов

    response = JSONResponse(
        content={"message": "Login successful", "username": user.username}
    )

    response.set_cookie("session_id", session_id)

    return response


@auth_router.get("/test-session") # type: ignore
async def get_user_info(
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    redis: aioredis.Redis = Depends(get_redis_async_conn),
) -> dict:
    user_id = await redis.get(session_id)
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    user_id = int(user_id)  # type: ignore

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    query = select(UsersOrm).filter(UsersOrm.id == user_id)
    result = await db_conn.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"user_id": user.id, "username": user.username}


@auth_router.post("/register") # type: ignore
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
            status_code=400, detail="User with such username already exists"
        )

    return {
        "message": "User created successfully",
        "username": new_user.username,
    }
