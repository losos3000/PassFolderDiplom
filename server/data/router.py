from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from server.configuration.basemodel import DefaultResponse
from server.data.schemas import (
    SDataAdd, SDataRead,
    SDataUserAccessAdd, SDataUserAccessRead,
    SDataRoleAccessAdd, SDataRoleAccessRead
)
from server.data.manager import DataManager, DataUserAccessManager, DataRoleAccessManager
from server.user.models import UserOrm
from server.user.manager import current_user

from cipher.cipher import cipher_manager

router = APIRouter()


###DATA API
@router.post("/add", response_model=DefaultResponse)
async def add_data(data: SDataAdd, user: UserOrm = Depends(current_user)):

    result = DefaultResponse(
        status="Success",
        data=None,
        message="Data record created",
        details=None,
    )

    try:
        data.login = cipher_manager.encrypt(data.login)
        data.password = cipher_manager.encrypt(data.password)
        data.url = cipher_manager.encrypt(data.url)
        data.description = cipher_manager.encrypt(data.description)
        data.name = cipher_manager.encrypt(data.name)

        await DataManager.add_data(data, user.id)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.get("/all", response_model=List[SDataRead])
async def read_data_my(user: UserOrm = Depends(current_user)):
    data_records: List[SDataRead] = await DataManager.read_data_my(user.id)

    for i in range(0, len(data_records), 1):
        data_records[i].login = cipher_manager.decrypt(data_records[i].login)
        data_records[i].password = cipher_manager.decrypt(data_records[i].password)
        data_records[i].url = cipher_manager.decrypt(data_records[i].url)
        data_records[i].description = cipher_manager.decrypt(data_records[i].description)
        data_records[i].name = cipher_manager.decrypt(data_records[i].name)

    return data_records


###USER ACCESSES API
@router.post("/user-access/add", response_model=DefaultResponse)
async def add_user_access(access: SDataUserAccessAdd):

    result = DefaultResponse(
        status="Success",
        data=None,
        message="Data access created",
        details=None,
    )

    try:
        await DataUserAccessManager.add_access(access)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.get("/access/all", response_model=List[SDataUserAccessRead])
async def read_user_access_all():
    accesses = await DataUserAccessManager.read_access_all()
    return accesses


###ROLE ACCESSES API
@router.post("/role-access/add", response_model=DefaultResponse)
async def add_role_access(access: SDataRoleAccessAdd):

    result = DefaultResponse(
        status="Success",
        data=None,
        message="Data access created",
        details=None,
    )

    try:
        await DataRoleAccessManager.add_access(access)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.get("/role-access/all", response_model=List[SDataRoleAccessRead])
async def read_role_access_all():
    accesses = await DataRoleAccessManager.read_access_all()
    return accesses
