from fastapi import APIRouter, Depends

from server.user.manager import auth_backend, fastapi_users, UserManager, current_user
from server.user.models import UserOrm
from server.user.schemas import UserRead, UserAdd

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserAdd),
)


@router.get("/me")
def protected_route(user: UserOrm = Depends(current_user)):
    return user
    # return {
    #     "status": "Success",
    #     "data": None,
    #     "message": f"Hello, {user.name}! Your id: {user.id}",
    #     "details": None,
    # }


@router.get("/all")
async def read_user_all():
    users = await UserManager.read_user_all()
    return {
        "status": "Success",
        "data": users,
        "message": "All users",
        "details": None,
    }
