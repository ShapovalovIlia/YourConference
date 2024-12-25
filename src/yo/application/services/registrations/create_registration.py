from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, Registration
from yo.application.exceptions import RegistrationAlreadyExistsError


class CreateRegistrationProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, user_id: int, conference_id: int) -> None:
        new_register = Registration(
            user_id=user_id, conference_id=conference_id
        )

        try:
            self._db_conn.add(new_register)
            await self._db_conn.commit()

        except IntegrityError:
            raise RegistrationAlreadyExistsError(
                message="A registration for this user on this conference already exists"
            )


def get_create_registrations_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> CreateRegistrationProcessor:
    return CreateRegistrationProcessor(db_conn=db_conn)
