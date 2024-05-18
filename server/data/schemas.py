from typing import Optional, List

from pydantic import BaseModel
from server.data.acccess.schemas import SDataUserAccessRead, SDataUserAccessEdit


###DATA SCHEMAS
class SDataAdd(BaseModel):
    name: str
    login: Optional[str]
    password: Optional[str]
    url: Optional[str]
    description: Optional[str]


class SDataRead(SDataAdd):
    id: int


class SDataWithAccessRead(SDataRead):
    access: List[SDataUserAccessRead]


class SDataDelete(BaseModel):
    id: int


class SDataEdit(BaseModel):
    id: int
    name: str | None
    login: str | None
    password: str | None
    url: str | None
    description: str | None
    access: List[SDataUserAccessEdit]


class SDataGet(BaseModel):
    id: int | None = None

class SData(SDataAdd):
    id: int
