from typing import Optional

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
