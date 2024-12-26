from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, Registration
from yo.application.exceptions import RegistrationAlreadyExistsError


class CreateRegistrationProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, user_id: UUID, conference_id: UUID) -> None:
        if await self._check_registration_exists(
            user_id=user_id, conference_id=conference_id
        ):
            raise RegistrationAlreadyExistsError(
                message="A registration for this user on this conference already exists"
            )

        new_register = Registration(
            user_id=user_id, conference_id=conference_id
        )

        self._db_conn.add(new_register)
        await self._db_conn.commit()

    async def _check_registration_exists(
        self, user_id: UUID, conference_id: UUID
    ) -> bool:
        query = select(Registration).where(
            Registration.user_id == user_id,
            Registration.conference_id == conference_id,
        )
        check = await self._db_conn.execute(query)

        return len(check.all()) > 0


def get_create_registrations_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> CreateRegistrationProcessor:
    return CreateRegistrationProcessor(db_conn=db_conn)
