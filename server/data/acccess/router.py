# from typing import List
#
# from fastapi import APIRouter, Depends
#
# from server.configuration.basemodel import DefaultResponse
#
# from server.user.models import UserOrm
# from server.user.manager import current_user, current_superuser
#
# from server.data.acccess.schemas import SDataUserAccessAdd, SDataUserAccessRead
# from server.data.acccess.manager import user_access_manager
#
#
# router = APIRouter()
#
#
# @router.post("/add", response_model=DefaultResponse)
# async def add_access(access: SDataUserAccessAdd, user: UserOrm = Depends(current_user)):
#
#     result = DefaultResponse(
#         status="Success",
#         data=None,
#         message="Data access created",
#         details=None,
#     )
#
#     try:
#         await user_access_manager.add_access(access)
#         return result
#
#     except Exception:
#         result.status = "500 Error"
#         result.message = "Internal server error"
#         return result
#
#
# @router.put("/edit", response_model=DefaultResponse)
# async def edit_access():
#
#     result = DefaultResponse(
#         status="Success",
#         data=None,
#         message=None,
#         details=None,
#     )
#
#     try:
#         # await user_access_manager.edit_access()
#         return result
#
#     except Exception:
#         result.status = "500 Error"
#         result.message = "Internal server error"
#         return result
#
#
# @router.delete("/delete", response_model=DefaultResponse)
# async def delete_access():
#
#     result = DefaultResponse(
#         status="Success",
#         data=None,
#         message=None,
#         details=None,
#     )
#
#     try:
#         # await user_access_manager.delete_access()
#         return result
#
#     except Exception:
#         result.status = "500 Error"
#         result.message = "Internal server error"
#         return result
#
#
# @router.get("/all", response_model=List[SDataUserAccessRead])
# async def read_access_all(user: UserOrm = Depends(current_superuser)):
#     accesses = await user_access_manager.read_access_all()
#     return accesses
#
#
# @router.get("/user/my", response_model=List[SDataUserAccessRead])
# async def read_access_my(user: UserOrm = Depends(current_user)):
#     accesses = await user_access_manager.read_access_for_user(user.id)
#     return accesses
#
#
# @router.get("/user/{user_id}", response_model=List[SDataUserAccessRead])
# async def read_access_user(user_id: int, user: UserOrm = Depends(current_user)):
#     accesses = await user_access_manager.read_access_for_user(user_id)
#     return accesses
#
#
# @router.get("/data/{data_id}", response_model=List[SDataUserAccessRead])
# async def read_access_data(data_id: int, user: UserOrm = Depends(current_user)):
#     accesses = await user_access_manager.read_access_for_data(data_id)
#     return accesses
