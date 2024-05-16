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