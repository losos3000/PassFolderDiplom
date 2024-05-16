from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from server.configuration.basemodel import Base


class UserOrm(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "ds_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]


class RoleToUserOrm(Base):
    __tablename__ = "ds_user_role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_user_id: Mapped[int] = mapped_column(ForeignKey("ds_user.id"))
    ds_role_id: Mapped[int] = mapped_column(ForeignKey("ds_role.id"))

