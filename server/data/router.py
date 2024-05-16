from typing import List

from fastapi import APIRouter, Depends

from server.configuration.basemodel import DefaultResponse

from server.user.models import UserOrm
from server.user.manager import current_user, current_superuser

from server.data.schemas import SDataAdd, SDataRead
from server.data.manager import data_manager


from cipher.cipher import cipher_manager

router = APIRouter()


def decrypt_data(data: List[SDataRead]) -> List[SDataRead]:
    for i in range(0, len(data), 1):
        data[i].login = cipher_manager.decrypt(data[i].login)
        data[i].password = cipher_manager.decrypt(data[i].password)
        data[i].url = cipher_manager.decrypt(data[i].url)
        data[i].description = cipher_manager.decrypt(data[i].description)
        data[i].name = cipher_manager.decrypt(data[i].name)
    return data


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

        await data_manager.add_data(data, user.id)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.put("/edit", response_model=DefaultResponse)
async def edit_data():
    result = DefaultResponse(
        status="Success",
        data=None,
        message=None,
        details=None,
    )

    try:
        # await DataUserAccessManager.edit_data(acess)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.delete("/delete", response_model=DefaultResponse)
async def delete_data():
    result = DefaultResponse(
        status="Success",
        data=None,
        message=None,
        details=None,
    )

    try:
        # await DataUserAccessManager.delete_data(acess)
        return result

    except Exception:
        result.status = "500 Error"
        result.message = "Internal server error"
        return result


@router.get("/all", response_model=List[SDataRead])
async def read_data_all(user: UserOrm = Depends(current_superuser)):
    data_records: List[SDataRead] = await data_manager.read_data_all()
    decrypt_data(data_records)
    return data_records


@router.get("/my", response_model=List[SDataRead])
async def read_data_my(user: UserOrm = Depends(current_user)):
    data_records: List[SDataRead] = await data_manager.read_data_accessed(user.id)
    decrypt_data(data_records)
    return data_records


@router.get("/{data_id}", response_model=List[SDataRead])
async def read_data(data_id: int, user: UserOrm = Depends(current_user)):
    data_records: List[SDataRead] = await data_manager.read_data(data_id)
    decrypt_data(data_records)
    return data_records
