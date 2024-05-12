from typing import Annotated

from fastapi import APIRouter, Depends

from server.role.schemas import SRoleAdd
from server.role.manager import RoleManager

router = APIRouter()


@router.post("/add")
async def add_role(role: SRoleAdd):
    role_id = await RoleManager.add_role(role)
    return {"message": "Role created!", "role_id": role_id}


@router.get("/all")
async def read_role_all():
    roles = await RoleManager.read_role_all()
    return {"roles": roles}
