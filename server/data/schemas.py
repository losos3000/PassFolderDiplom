from typing import Optional

from pydantic import BaseModel
from sqlalchemy import JSON


class SDataAdd(BaseModel):
    login: Optional[str]
    password: Optional[str]
    url: Optional[str]
    description: Optional[str]
    # ds_user_id: Optional[int]


class SDataRead(SDataAdd):
    id: int


class SDataUserAccessAdd(BaseModel):
    ds_data_id: int
    ds_user_id: int
    access_read: Optional[bool]
    access_edit: Optional[bool]


class SDataUserAccessRead(SDataUserAccessAdd):
    pass
