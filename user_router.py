from typing import Annotated

from fastapi import APIRouter, Depends

from repository import UserRepository
from schemas import SUserAdd

router = APIRouter()


@router.post("/user/add")
async def add_user(user: Annotated[SUserAdd, Depends()]):
    user_id = await UserRepository.add_user(user)
    return {"message": "User created!", "user_id": user_id}


@router.get("/user/all")
async def show_all_users():
    users = await UserRepository.show_all_users()
    return {"users": users}
