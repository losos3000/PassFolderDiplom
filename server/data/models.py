from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from server.configuration.basemodel import Base


class DataOrm(Base):
    __tablename__ = "ds_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[Optional[str]]
    password: Mapped[Optional[str]]
    url: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    user_access: Mapped[Optional[str]]
    role_access: Mapped[Optional[str]]
