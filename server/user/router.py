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
    current_user, current_superuser, current_user_token)

from server.user.models import UserOrm
from server.user.schemas import SUserRead, SUserAdd, SUserRead, SUserDelete, SUserEdit, SUserAuth

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

@router.post("/add", response_model=DefaultResponse, status_code=status.HTTP_201_CREATED)
async def register(
        request: Request,
        new_user: SUserAdd,
        # user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
        user: UserOrm = Depends(current_superuser),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_201_CREATED,
        data=None,
        message="OK",
        details="Пользователь успешно создан",
    )

    try:
        await UserManager.add_user(user_create=new_user, safe=True, request=request)
    except exceptions.UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL SERVER ERROR"
        )
    return response


@router.post("/login")
async def login(
    request: Request,
    data: SUserAuth,
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    response = DefaultResponse(
        status="Success",
        status_code=status.HTTP_200_OK,
        data=None,
        message="OK",
        details="Аутентификация прошла успешна",
    )

    # try:
    user = await UserManager.authenticate(data)
    print(user)
    if user is None: # or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
    res = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, res)

    # except HTTPException as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
    #     )
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="INTERNAL SERVER ERROR"
    #     )
    return response


@router.post("/logout")
async def logout(
    user_token: Tuple[models.UP, str] = Depends(current_user_token),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)


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
        await UserManager.edit_user()
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


@router.get("/all", response_model=List[SUserRead], status_code=status.HTTP_200_OK)
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


@router.get("/{user_id}", response_model=List[SUserRead], status_code=status.HTTP_200_OK)
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

