from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_helper
from users.models.user import User
from users.models.user_manager import UserManager


async def get_user_db(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    yield User.get_db(session=session)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
