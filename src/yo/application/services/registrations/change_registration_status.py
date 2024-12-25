from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from yo.application.postgres import (
    get_postgres_async_conn,
    Registration,
    Admin,
)
from yo.application.exceptions import (
    UknownSessionIdError,
    PermissionError,
    RegistrationNotFoundError,
)


class ChangeRegistrationStatusProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(
        self, *, admin_id: int, registration_id: int, recommended: bool
    ) -> None:
        if not admin_id:
            raise UknownSessionIdError(message="Session expired or invalid")

        if await self._db_conn.get(Admin, admin_id) is None:
            raise PermissionError(
                message="You don't have permission to change register status",
            )

        registration = await self._db_conn.get(Registration, registration_id)
        if not registration:
            raise RegistrationNotFoundError(message="Registration not found")

        registration.recommended = recommended
        await self._db_conn.commit()


def get_change_registration_status_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> ChangeRegistrationStatusProcessor:
    return ChangeRegistrationStatusProcessor(db_conn=db_conn)
