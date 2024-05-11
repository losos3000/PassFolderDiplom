from fastapi import APIRouter

from server.user.manager import auth_backend, fastapi_users
from server.user.schemas import UserRead, UserAdd

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserAdd),
)


# @router.get("/all")
# async def read_user_all():
#     users = await UserRepository.read_user_all()
#     return {"users": users}
