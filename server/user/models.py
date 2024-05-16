from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from server.configuration.basemodel import Base


class UserOrm(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "ds_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
