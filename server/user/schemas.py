from fastapi_users import schemas
from pydantic import BaseModel


###USER SCHEMAS
class SUserRead(schemas.BaseUser[int]):
    name: str


class SUserAdd(schemas.BaseUserCreate):
    name: str


class SUserUpdate(schemas.BaseUserUpdate):
    pass


###ROLE FOR USER SCHEMAS
class SRoleToUserAdd(BaseModel):
    ds_user_id: int
    ds_role_id: int

class SRoleToUserRead(SRoleToUserAdd):
    pass