from typing import Annotated

from fastapi import APIRouter, Depends

from models.repository import UserRepository
# from models.schemas import SUserAdd

router = APIRouter()


# @router.post("/add")
# async def add_user(user: Annotated[SUserAdd, Depends()]):
#     user_id = await UserRepository.add_user(user)
#     return {"message": "User created!", "user_id": user_id}


@router.get("/all")
async def read_user_all():
    users = await UserRepository.read_user_all()
    return {"users": users}
