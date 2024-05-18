from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from server.configuration.basemodel import DefaultResponse

from server.user.models import UserOrm
from server.user.manager import current_user

from server.data.schemas import SDataAdd, SDataDelete, SDataEdit, SDataGet, SDataWithAccessRead
from server.data.manager import data_manager

from cipher.cipher import cipher_manager

router = APIRouter()


def decrypt_data(data: List[SDataWithAccessRead]) -> List[SDataWithAccessRead]:
    for i in range(0, len(data), 1):
        if data[i].login is not None:
            data[i].login = cipher_manager.decrypt(data[i].login)
        if data[i].password is not None:
            data[i].password = cipher_manager.decrypt(data[i].password)
        if data[i].url is not None:
            data[i].url = cipher_manager.decrypt(data[i].url)
        if data[i].description is not None:
            data[i].description = cipher_manager.decrypt(data[i].description)
        if data[i].name is not None:
            data[i].name = cipher_manager.decrypt(data[i].name)
    return data


def encrypt_data(data: SDataAdd | SDataEdit) -> SDataAdd | SDataEdit:
    if data.login is not None:
        data.login = cipher_manager.encrypt(data.login)
    if data.password is not None:
        data.password = cipher_manager.encrypt(data.password)
    if data.url is not None:
        data.url = cipher_manager.encrypt(data.url)
    if data.description is not None:
        data.description = cipher_manager.encrypt(data.description)
    if data.name is not None:
        data.name = cipher_manager.encrypt(data.name)
    return data


@router.post("/add", response_model=DefaultResponse, status_code=status.HTTP_201_CREATED)
async def add_data(
        data: SDataAdd,
        user: UserOrm = Depends(current_user)
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_201_CREATED,
        detail="CREATED",
        message="Данные успешно созданы",
        data=None,
    )
    try:
        await data_manager.add_data(
            data=encrypt_data(data),
            user=user
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.put("/edit", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def edit_data(
        data: SDataEdit,
        user: UserOrm = Depends(current_user),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        detail="OK",
        message="Запись данных успешно изменена",
        data=None,
    )
    try:
        await data_manager.edit_data(
            new_data=encrypt_data(data),
            user=user,
        )
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.delete("/delete", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def delete_data(
        data: SDataDelete,
        user: UserOrm = Depends(current_user),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        detail="OK",
        message="Данные успешно удалены",
        data=None,
    )
    try:
        await data_manager.delete_data(data.id, user)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.get("/my", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def read_data_my(
        user: UserOrm = Depends(current_user),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        detail="OK",
        message="Доступные запси данных успешно получены",
        data=None,
    )
    data = SDataGet(
        id=None,
    )
    try:
        data_records: List[SDataWithAccessRead] = await data_manager.read_data(
            user=user,
            data=data,
        )
        response.data = decrypt_data(data_records)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.get("/id", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def read_data_id(
        data: SDataGet,
        user: UserOrm = Depends(current_user),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        detail="OK",
        message="Запись данных успешно получены",
        data=None,
    )
    try:
        data_records: List[SDataWithAccessRead] = await data_manager.read_data(
            user=user,
            data=data,
        )
        response.data = decrypt_data(data_records)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response
