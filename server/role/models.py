from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from server.configuration.basemodel import Base


class RoleOrm(Base):
    __tablename__ = "ds_role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    permission: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
