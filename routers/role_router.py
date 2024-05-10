# from typing import Annotated
#
# from fastapi import APIRouter, Depends
#
# from models.repository import RoleRepository
# from models.schemas import SRoleAdd
#
# router = APIRouter()
#
#
# @router.post("/add")
# async def add_role(role: Annotated[SRoleAdd, Depends()]):
#     role_id = await RoleRepository.add_role(role)
#     return {"message": "Role created!", "role_id": role_id}
#
#
# @router.get("/all")
# async def read_role_all():
#     roles = await RoleRepository.read_role_all()
#     return {"roles": roles}
