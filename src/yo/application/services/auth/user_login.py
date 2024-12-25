from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, User
from yo.application.exceptions import WrongPasswordOrUsernameError


class UserLoginProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, username: str, password: str) -> int:
        query = select(User).where(User.username == username)
        result = await self._db_conn.execute(query)
        user = result.scalar_one_or_none()

        if user is None or password != user.password:
            raise WrongPasswordOrUsernameError(
                message="Incorrect username or password"
            )

        return user.id


def get_user_login_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> UserLoginProcessor:
    return UserLoginProcessor(db_conn=db_conn)
