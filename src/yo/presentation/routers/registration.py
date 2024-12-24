from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, Cookie, Query

from yo.application import (
    get_postgres_async_conn,
    AsyncSessionManager,
    Registration,
    Admin,
    get_session_manager,
)


registration_router = APIRouter(prefix="/registrations")


@registration_router.post("")  # type: ignore
async def register(
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    session_id: str = Cookie(...),
    conference_id: int = Query(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    new_register = Registration(user_id=user_id, conference_id=conference_id)

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


@registration_router.delete("/{registration_id}")  # type: ignore
async def delete_register(
    registration_id: int,
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    query = select(Registration).where(Registration.id == registration_id)
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


@registration_router.put("/{registration_id}/status")  # type: ignore #TODO айди админов и юзеров пересекаются
async def change_register_status(
    registration_id: int,
    recommended: bool = Query(...),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    session_id: str = Cookie(...),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> dict:
    admin_id = await session_manager.get_user_id(session_id)

    if not admin_id:
        raise HTTPException(
            status_code=401, detail="Session expired or invalid"
        )

    if await db_conn.get(Admin, admin_id) is None:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to change register status",
        )

    registration = await db_conn.get(Registration, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    registration.recommended = recommended
    await db_conn.commit()

    return {"detail": "Registration status updated successfully"}
