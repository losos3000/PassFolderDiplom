from typing import Optional

from pydantic import BaseModel
from sqlalchemy import JSON


class SRoleAdd(BaseModel):
    name: str
    permission: Optional[str]
    description: Optional[str]


class SRoleRead(SRoleAdd):
    id: int
    description: str
