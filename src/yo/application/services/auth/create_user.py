from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, User
from yo.application.exceptions import UserAlreadyExistsError


class CreateUserProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, username: str, password: str) -> None:
        new_user = User(username=username, password=password)

        try:
            self._db_conn.add(new_user)
            await self._db_conn.commit()

        except IntegrityError:
            raise UserAlreadyExistsError(
                message="User with such username already exists"
            )


def get_create_user_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> CreateUserProcessor:
    return CreateUserProcessor(db_conn=db_conn)
