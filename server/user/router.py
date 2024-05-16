from typing import List

from fastapi import APIRouter, Depends

from server.configuration.basemodel import DefaultResponse
from server.role.schemas import SRoleRead
from server.user.manager import auth_backend, fastapi_users, UserManager, current_user, UserRoleManager
from server.user.models import UserOrm
from server.user.schemas import SUserRead, SUserAdd, SUserRead, SRoleToUserRead, SRoleToUserAdd

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(SUserRead, SUserAdd),
)


###USERS
@router.get("/me", response_model=SUserRead)
def read_user_me(user: UserOrm = Depends(current_user)):
    return user


@router.get("/all", response_model=List[SUserRead])
async def read_user_all():
    users = await UserManager.read_user_all()
    return users


###ROLES TO USERS
@router.post("/role/add", response_model=DefaultResponse)
async def add_user_role(role: SRoleToUserAdd):

    result = DefaultResponse(
        status="Success",
        data=None,
        message="Role added",
        details=None,
    )

    try:
        await UserRoleManager.add_user_role(role)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.get("/role/me", response_model=List[SRoleRead])
async def read_user_role_me(user: UserOrm = Depends(current_user)):
    roles = await UserManager.read_user_role_me(user.id)
    return roles


@router.get("/role/all", response_model=List[SRoleToUserRead])
async def read_user_role_all():
    roles = await UserManager.read_user_role_all()
    return roles
