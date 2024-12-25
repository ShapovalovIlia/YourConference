from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import Depends

from yo.application.postgres import get_postgres_async_conn, Admin
from yo.application.exceptions import WrongPasswordOrUsernameError


class AdminLoginProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(self, *, username: str, password: str) -> int:
        query = select(Admin).where(Admin.username == username)
        result = await self._db_conn.execute(query)
        admin = result.scalar_one_or_none()

        if admin is None or password != admin.password:
            raise WrongPasswordOrUsernameError(
                message="Incorrect username or password"
            )

        return admin.id


def get_admin_login_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> AdminLoginProcessor:
    return AdminLoginProcessor(db_conn=db_conn)
