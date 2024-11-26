from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from core import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass
