from typing import Optional

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from server.configuration.basemodel import Base


class DataOrm(Base):
    __tablename__ = "ds_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(default="Мои данные")
    login: Mapped[Optional[str]]
    password: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    description: Mapped[Optional[str]]


class DataUserAccessOrm(Base):
    __tablename__ = "ds_data_user_access"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_data_id: Mapped[int] = mapped_column(ForeignKey("ds_data.id"))
    ds_user_id: Mapped[int] = mapped_column(ForeignKey("ds_user.id"))
    access_read: Mapped[bool] = mapped_column(default=False)
    access_edit: Mapped[bool] = mapped_column(default=False)


class DataRoleAccessOrm(Base):
    __tablename__ = "ds_data_role_access"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ds_data_id: Mapped[int] = mapped_column(ForeignKey("ds_data.id"))
    ds_role_id: Mapped[int] = mapped_column(ForeignKey("ds_role.id"))
    access_read: Mapped[bool] = mapped_column(default=False)
    access_edit: Mapped[bool] = mapped_column(default=False)
