from fastapi import Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from users.auth_backend import authentication_backend
from users.models.user import User
from users.models.user_manager import UserManager


async def get_user_db(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    yield User.get_db(session=session)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)

current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_active_verified_superuser = fastapi_users.current_user(
    active=True, verified=True, superuser=True
)
