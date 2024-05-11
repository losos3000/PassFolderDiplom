from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    name: str
    pass


class UserAdd(schemas.BaseUserCreate):
    name: str
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass



# from typing import Optional
#
# from pydantic import BaseModel
# from fastapi_users import schemas
#
#
# class SUserRead(schemas.BaseUser[int]):
#     id: int
#     login: str
#     email: str
#     is_active: bool = True
#     is_superuser: bool = False
#     is_verified: bool = False
#     pass
#
#
# class SUserAdd(schemas.BaseUserCreate):
#     name: str
#     login: str
#     role_id: int
#     pass
#
#
# # class UserUpdate(schemas.BaseUserUpdate):
# #     pass
#
#

