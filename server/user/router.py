from typing import List, Type, Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_users import schemas, exceptions, models
from fastapi_users.authentication import Strategy, Authenticator
from fastapi_users.manager import BaseUserManager
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode

from server.configuration.basemodel import DefaultResponse
from server.user.manager import (
    auth_backend, fastapi_users, UserManager, get_user_manager,
    current_user, current_superuser)

from server.user.models import UserOrm
from server.user.schemas import SUserRead, SUserAdd, SUserRead, SUserDelete, SUserEdit, SUserAuth

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(SUserRead, SUserAdd),
)


@router.put("/edit", response_model=DefaultResponse,status_code=status.HTTP_200_OK)
async def edit_user(
        data: SUserEdit,
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
        user: UserOrm = Depends(current_superuser),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        data=None,
        message="OK",
        details="Пользователь успешно изменен",
    )
    try:
        await UserManager.edit_user(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response

@router.delete("/delete", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def delete_user(data: SUserDelete, user: UserOrm = Depends(current_superuser)):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        data=None,
        message="OK",
        details="Пользователь успешно удален",
    )
    try:
        await UserManager.delete_user(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.get("/all", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def read_user_all(user: UserOrm = Depends(current_user)):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        data=None,
        message="OK",
        details="Даные всех пользователей",
    )
    try:
        response.data = await UserManager.read_user_all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.get("/me", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def read_user_me(user: UserOrm = Depends(current_user)):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        data=None,
        message="OK",
        details="Даные аутентифицированного пользователя",
    )
    try:
        response.data = await UserManager.read_user(user.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.get("/{user_id}", response_model=DefaultResponse, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, user: UserOrm = Depends(current_user)):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        data=None,
        message="OK",
        details="Даные выбранного пользователя",
    )
    try:
        response.data = await UserManager.read_user(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response

