from typing import Annotated, List

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from server.data.schemas import SDataAdd, SDataUserAccessAdd, SDataRead
from server.data.manager import DataManager, DataUserAccessManager, current_user
from server.user.models import UserOrm

from cipher.cipher import cipher_manager

router = APIRouter()



@router.post("/add")
async def add_data(data: SDataAdd, user: UserOrm = Depends(current_user)):
    # user: UserOrm = Depends(current_user)
    print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA{data.login}")
    data.login = cipher_manager.encrypt(data.login)
    # data.password = cipher_manager.encrypt(data.password)
    print(f"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB{data.login}")

    await DataManager.add_data(data, user.id)
    return {
        "status": "Success",
        "data": None,
        "message": "Data record created",
        "details": None,
    }


@router.get("/all", response_model=List[SDataRead])
async def read_data_all(user: UserOrm = Depends(current_user)):
    data_records: SDataRead = await DataManager.read_data_all(user.id)
    return {
        "status": "Success",
        "data": data_records,
        "message": "All data accesses",
        "details": None,
    }


@router.post("/access/add")
async def add_user_access(access: SDataUserAccessAdd):
    await DataUserAccessManager.add_access(access)
    return {
        "status": "Success",
        "data": None,
        "message": "Data access created",
        "details": None,
    }


@router.get("/access/all")
async def read_user_access_all():
    accesses = await DataUserAccessManager.read_access_all()
    return {
        "status": "Success",
        "data": accesses,
        "message": "All data accesses",
        "details": None,
    }
