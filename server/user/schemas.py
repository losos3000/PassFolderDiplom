from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


###USER SCHEMAS
class SUserAdd(schemas.BaseUserCreate):
    name: str


class SUserRead(schemas.BaseUser[int]):
    name: str


class SUserEdit(BaseModel):
    id: int
    email: EmailStr | None = None
    name: str | None = None
    password: str | None = None
    is_superuser: bool | None = None


class SUserDelete(BaseModel):
    id: int


class SUserAuth(BaseModel):
    email: str
    password: str


class SUser(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

