from fastapi import Depends

from server.user.manager import fastapi_users
from sqlalchemy import select

from server.configuration.database import session_factory
from server.data.models import DataOrm, DataUserAccessOrm
from server.data.schemas import SDataAdd, SDataUserAccessAdd

current_user = fastapi_users.current_user()


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
            return access_model


user_access_manager = DataUserAccessManager()


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
    async def read_data_all(cls, user_id: int):
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
            return ds_data_model

    @classmethod
    async def read_accessed_data(cls):
        async with session_factory() as session:
            query = select(DataOrm)
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            return ds_data_model
