from typing import Optional

from pydantic import BaseModel


###USERS ACCESSES SCHEMAS
class SDataUserAccessAdd(BaseModel):
    ds_data_id: int
    ds_user_id: int
    access_read: Optional[bool]
    access_edit: Optional[bool]


class SDataUserAccessRead(SDataUserAccessAdd):
    pass


###ROLES ACCESSES SCHEMAS
class SDataRoleAccessAdd(BaseModel):
    ds_data_id: int
    ds_role_id: int
    access_read: Optional[bool]
    access_edit: Optional[bool]


class SDataRoleAccessRead(SDataRoleAccessAdd):
    pass


###DATA SCHEMAS
class SDataAdd(BaseModel):
    name: str
    login: Optional[str]
    password: Optional[str]
    url: Optional[str]
    description: Optional[str]


class SDataRead(SDataAdd):
    id: int
