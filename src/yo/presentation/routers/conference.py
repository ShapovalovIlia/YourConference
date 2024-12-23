import redis.asyncio as aioredis  # type: ignore

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, Cookie, Query

from yo.infrastructure import (
    get_postgres_async_conn,
    get_redis_async_conn,
    ConferencesOrm,
    AsyncSessionManager,
    RegistrationsOrm,
    AdminsOrm,
)


conference_router = APIRouter(prefix="/conferences")


@conference_router.get("") # type: ignore
async def get_conferences_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> list[ConferencesOrm]:
    query = select(ConferencesOrm).offset(skip).limit(limit)
    conferences = await db_conn.execute(query)
    return conferences


@conference_router.post("/registrations/register") # type: ignore
async def register(
    redis: aioredis.Redis = Depends(get_redis_async_conn),
    session_id: str = Cookie(...),
    conference_id: int = Query(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    session_manager = AsyncSessionManager(redis=redis)
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    user_id = int(user_id)  # type: ignore

    new_register = RegistrationsOrm(
        user_id=user_id, conference_id=conference_id
    )

    try:
        db_conn.add(new_register)
        await db_conn.commit()
        await db_conn.refresh(new_register)

    except IntegrityError:
        await db_conn.rollback()

        raise HTTPException(
            status_code=400, detail="Such register already exists"
        )

    return {
        "message": "Registration created successfully",
    }


@conference_router.delete("/registrations/register/{registration_id}") # type: ignore
async def delete_register(
    registration_id: int,  # Указываем тип данных
    redis: aioredis.Redis = Depends(get_redis_async_conn),
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    session_manager = AsyncSessionManager(redis=redis)
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    query = select(RegistrationsOrm).where(
        RegistrationsOrm.id == registration_id
    )
    result = await db_conn.execute(query)
    registration = result.scalar_one_or_none()

    if not registration:
        raise HTTPException(
            status_code=400, detail="There is no such registration"
        )

    if registration.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have sufficient permissions to delete this record",
        )

    await db_conn.delete(registration)
    await db_conn.commit()

    return {"message": "Registration deleted successfully"}


@conference_router.patch("/change-status/{registration_id}") # type: ignore
async def change_register_status(
    registration_id: int,
    recommended: bool = Query(...),
    redis: aioredis.Redis = Depends(get_redis_async_conn),
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    # Проверка сессии
    session_manager = AsyncSessionManager(redis=redis)
    admin_id = await session_manager.get_user_id(session_id)

    if not admin_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    admin_id = int(admin_id)  # type: ignore
    if await db_conn.get(AdminsOrm, admin_id) is None:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to change register status",
        )

    # Получаем запись и обновляем её
    registration = await db_conn.get(RegistrationsOrm, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.recommended = recommended
    await db_conn.commit()

    return {"detail": "Registration status updated successfully"}
