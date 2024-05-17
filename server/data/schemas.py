from typing import Optional

from pydantic import BaseModel


###DATA SCHEMAS
class SDataAdd(BaseModel):
    name: str
    login: Optional[str]
    password: Optional[str]
    url: Optional[str]
    description: Optional[str]


class SDataRead(SDataAdd):
    id: int


class SDataDelete(BaseModel):
    id: int
