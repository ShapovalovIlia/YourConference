from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, Registration
from yo.application.exceptions import RegistrationNotFoundError


class DeleteRegistrationProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, user_id: UUID, registration_id: UUID) -> None:
        query = select(Registration).where(Registration.id == registration_id)
        result = await self._db_conn.execute(query)
        registration = result.scalar_one_or_none()

        if not registration:
            raise RegistrationNotFoundError(
                message="There is no such registration"
            )

        if registration.user_id != user_id:
            raise RegistrationNotFoundError(
                message="You do not have sufficient permissions to delete this record",
            )

        await self._db_conn.delete(registration)
        await self._db_conn.commit()


def get_delete_registrations_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> DeleteRegistrationProcessor:
    return DeleteRegistrationProcessor(db_conn=db_conn)
