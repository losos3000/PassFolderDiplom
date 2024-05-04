from typing import Optional

from pydantic import BaseModel


class SUserAdd(BaseModel):
    name: str
    login: str
    password: str
    description: Optional[str]


class SUserRead(SUserAdd):
    id: int
