from typing import List

from pydantic import TypeAdapter
from sqlalchemy import select

from server.configuration.database import session_factory

from server.data.acccess.models import DataUserAccessOrm
from server.data.acccess.schemas import SDataUserAccessAdd, SDataUserAccessRead


class DataUserAccessManager:
    @classmethod
    async def add_access_with_session(cls, data: SDataUserAccessAdd, session):
        access_dict = data.model_dump()
        access = DataUserAccessOrm(**access_dict)
        session.add(access)
        await session.flush()

    @classmethod
    async def add_access(cls, data: SDataUserAccessAdd):
        async with session_factory() as session:
            access_dict = data.model_dump()
            access = DataUserAccessOrm(**access_dict)
            session.add(access)
            await session.flush()
            await session.commit()

    @classmethod
    async def read_access_all(cls):
        async with session_factory() as session:
            query = select(DataUserAccessOrm)
            result = await session.execute(query)
            access_model = result.scalars().all()
            access_schema = [SDataUserAccessRead.model_validate(ras, from_attributes=True) for ras in access_model]
            return access_schema

    @classmethod
    async def read_access_for_data(cls, data_id: int):
        async with session_factory() as session:
            query = select(DataUserAccessOrm).where(DataUserAccessOrm.ds_data_id == data_id)
            result = await session.execute(query)
            access_model = result.scalars().all()
            access_schema = [SDataUserAccessRead.model_validate(ras, from_attributes=True) for ras in access_model]
            return access_schema

    @classmethod
    async def read_access_for_user(cls, user_id: int):
        async with session_factory() as session:
            query = select(DataUserAccessOrm).where(DataUserAccessOrm.ds_user_id == user_id)
            result = await session.execute(query)
            access_model = result.scalars().all()
            access_schema = [SDataUserAccessRead.model_validate(ras, from_attributes=True) for ras in access_model]
            return access_schema


user_access_manager = DataUserAccessManager()