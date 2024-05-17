from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from server.configuration.basemodel import DefaultResponse

from server.user.models import UserOrm
from server.user.manager import current_user, current_superuser

from server.data.schemas import SDataAdd, SDataRead, SDataDelete, SDataEdit, SDataGet
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
    # try:
    data.login = cipher_manager.encrypt(data.login)
    data.password = cipher_manager.encrypt(data.password)
    data.url = cipher_manager.encrypt(data.url)
    data.description = cipher_manager.encrypt(data.description)
    data.name = cipher_manager.encrypt(data.name)
    await data_manager.add_data(data, user.id)
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="INTERNAL SERVER ERROR"
    #     )
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
        message="Пользователь успешно изменен",
        data=None,
    )
    try:
        # response.data = await DataUserAccessManager.edit_data(acess)
        ...
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
async def read_data(
        data: SDataGet,
        user: UserOrm = Depends(current_user),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        detail="OK",
        message="Все данные успешно получены",
        data=None,
    )
    # try:
    data_records: List[SDataRead] = await data_manager.read_data(user, data)
    response.data = decrypt_data(data_records)
    # except HTTPException as e:
    #     raise HTTPException(
    #         status_code=e.status_code,
    #         detail=e.detail
    #     )
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="INTERNAL SERVER ERROR"
    #     )
    return response


# @router.get("/my", response_model=List[SDataRead])
# async def read_data_my(user: UserOrm = Depends(current_user)):
#     response = DefaultResponse(
#         status="Success",
#         status_code=status.HTTP_200_OK,
#         detail="OK",
#         message="Ваши данные успешно получены",
#         data=None,
#     )
#     try:
#         data_records: List[SDataRead] = await data_manager.read_data_accessed(user.id)
#         response.data = decrypt_data(data_records)
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code,
#             detail=e.detail
#         )
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="INTERNAL SERVER ERROR"
#         )
#     return response
#
#
# @router.get("/{data_id}", response_model=List[SDataRead])
# async def read_data(
#         data_id: int,
#         user: UserOrm = Depends(current_user),
# ):
#     response = DefaultResponse(
#         status="Success",
#         status_code=status.HTTP_200_OK,
#         detail="OK",
#         message="Данные записи успешно получены",
#         data=None,
#     )
#     try:
#         data_records: List[SDataRead] = await data_manager.read_data(data_id)
#         response.data = decrypt_data(data_records)
#     except HTTPException as e:
#         raise HTTPException(
#             status_code=e.status_code,
#             detail=e.detail
#         )
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="INTERNAL SERVER ERROR"
#         )
#     return response
