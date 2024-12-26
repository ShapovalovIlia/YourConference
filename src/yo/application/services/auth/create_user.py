from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, User
from yo.application.exceptions import UserAlreadyExistsError


class CreateUserProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, username: str, password: str) -> None:
        if await self._check_user_exists(username):
            raise UserAlreadyExistsError(
                message="User with such username already exists"
            )

        new_user = User(username=username, password=password)
        self._db_conn.add(new_user)
        await self._db_conn.commit()

    async def _check_user_exists(self, username: str) -> bool:
        query = select(User).where(User.username == username)
        check = await self._db_conn.execute(query)

        return len(check.all()) > 0


def get_create_user_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> CreateUserProcessor:
    return CreateUserProcessor(db_conn=db_conn)
