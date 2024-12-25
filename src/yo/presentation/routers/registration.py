from fastapi import APIRouter, HTTPException, Depends, Cookie, Query

from yo.application import (
    AsyncSessionManager,
    Registration,
    Admin,
    get_session_manager,
    CreateRegistrationProcessor,
    get_create_registrations_processor,
    DeleteRegistrationProcessor,
    get_delete_registrations_processor,
    ChangeRegistrationStatusProcessor,
    get_change_registration_status_processor,
)


registration_router = APIRouter(prefix="/registrations")


@registration_router.post("")  # type: ignore
async def register(
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    session_id: str = Cookie(...),
    conference_id: int = Query(),
    processor: CreateRegistrationProcessor = Depends(
        get_create_registrations_processor
    ),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)
    await processor.process(
        user_id=user_id,
        conference_id=conference_id,
    )
    return {
        "message": "Registration created successfully",
    }


@registration_router.delete("/{registration_id}")  # type: ignore
async def delete_register(
    registration_id: int,
    session_id: str = Cookie(...),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    processor: DeleteRegistrationProcessor = Depends(
        get_delete_registrations_processor
    ),
) -> dict:
    user_id = await session_manager.get_user_id(session_id)
    await processor.process(user_id=user_id, registration_id=registration_id)

    return {"message": "Registration deleted successfully"}


@registration_router.put("/{registration_id}/status")  # type: ignore # TODO айди админов и юзеров пересекаются
async def change_registration_status(
    registration_id: int,
    recommended: bool = Query(...),
    session_manager: AsyncSessionManager = Depends(get_session_manager),
    session_id: str = Cookie(...),
    processor: ChangeRegistrationStatusProcessor = Depends(
        get_change_registration_status_processor
    ),
) -> dict:
    admin_id = await session_manager.get_user_id(session_id)

    await processor.process(
        admin_id=admin_id,
        recommended=recommended,
        registration_id=registration_id,
    )

    return {"detail": "Registration status updated successfully"}
