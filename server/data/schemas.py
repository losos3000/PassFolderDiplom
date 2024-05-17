from typing import Optional, List

from pydantic import BaseModel
from server.data.acccess.schemas import SDataUserAccessRead


###DATA SCHEMAS
class SDataAdd(BaseModel):
    name: str
    login: Optional[str]
    password: Optional[str]
    url: Optional[str]
    description: Optional[str]


class SDataRead(SDataAdd):
    id: int
    access: List[SDataUserAccessRead]


class SDataDelete(BaseModel):
    id: int

class SDataEdit(SDataRead):
    pass

class SDataGet(BaseModel):
    id: int | None = None
