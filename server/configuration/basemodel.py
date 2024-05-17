from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

from server.data.acccess.schemas import SDataUserAccessRead
from server.data.schemas import SDataRead
from server.user.schemas import SUserRead


class Base(DeclarativeBase):
    pass


class DefaultResponse(BaseModel):
    status: str = "None"
    status_code: int = 0
    detail: str | None = None
    message: str | None = None
    data: List[SUserRead] | List[SDataRead] | List[SDataUserAccessRead] | None = None



