from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DefaultResponse(BaseModel):
    status: str | None
    data: list | dict | object | None
    message: str | None
    details: str | None