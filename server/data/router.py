from typing import Annotated

from fastapi import APIRouter, Depends

from server.data.schemas import SDataAdd
from server.data.manager import DataManager

router = APIRouter()


@router.post("/add")
async def add_data(role: Annotated[SDataAdd, Depends()]):
    role_id = await DataManager.add_data(role)
    return {"message": "Data record created!", "ds_data_id": role_id}


@router.get("/all")
async def read_data_all():
    roles = await DataManager.read_data_all()
    return {"Data records": roles}
