from typing import Optional

from pydantic import BaseModel
from sqlalchemy import JSON


class SDataAdd(BaseModel):
    login: Optional[str]
    password: Optional[str]
    url: Optional[str]
    description: Optional[str]
    user_access: Optional[str]
    role_access: Optional[str]


class SDataRead(SDataAdd):
    id: int

