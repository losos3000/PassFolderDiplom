from typing import List

from pydantic import TypeAdapter
from sqlalchemy import select

from server.configuration.database import session_factory

from server.data.acccess.manager import user_access_manager
from server.data.acccess.models import DataUserAccessOrm
from server.data.acccess.schemas import SDataUserAccessAdd

from server.data.models import DataOrm
from server.data.schemas import SDataAdd, SDataRead


data_ta = TypeAdapter(List[SDataRead])


class DataManager:
    @classmethod
    async def add_data(cls, data: SDataAdd, user_id: int):
        async with session_factory() as session:
            ds_data_dict = data.model_dump()
            ds_data = DataOrm(**ds_data_dict)
            session.add(ds_data)
            await session.flush()

            user_access = SDataUserAccessAdd(
                ds_data_id=ds_data.id,
                ds_user_id=user_id,
                access_read=True,
                access_edit=True,
            )
            await user_access_manager.add_access_with_session(user_access, session)

            await session.commit()

    @classmethod
    async def read_data_accessed(cls, user_id: int):
        async with session_factory() as session:
            query = (
                select(DataOrm)
                .join(
                    DataUserAccessOrm,
                    DataUserAccessOrm.ds_data_id == DataOrm.id,
                ).filter(
                    DataUserAccessOrm.ds_user_id == user_id,
                )
            )
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            ds_data_schema = [SDataRead.model_validate(ddm, from_attributes=True) for ddm in ds_data_model]
            return ds_data_schema

    @classmethod
    async def read_data_all(cls):
        async with session_factory() as session:
            query = select(DataOrm)
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            ds_data_schema = [SDataRead.model_validate(ddm, from_attributes=True) for ddm in ds_data_model]
            return ds_data_schema

    @classmethod
    async def read_data(cls, data_id: int):
        async with session_factory() as session:
            query = select(DataOrm).where(DataOrm.id == data_id)
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            ds_data_schema = [SDataRead.model_validate(ddm, from_attributes=True) for ddm in ds_data_model]
            return ds_data_schema


data_manager = DataManager()
