from typing import List

from fastapi import Depends
from pydantic import TypeAdapter
from sqlalchemy import select

from server.configuration.database import session_factory
from server.user.manager import fastapi_users
from server.data.models import DataOrm, DataUserAccessOrm, DataRoleAccessOrm
from server.data.schemas import SDataAdd, SDataRead, SDataUserAccessAdd, SDataRoleAccessAdd, SDataRoleAccessRead

current_user = fastapi_users.current_user()

data_ta = TypeAdapter(List[SDataRead])


###USER ACCESS MANAGER
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
            access_schema = [SDataRoleAccessRead.model_validate(ras, from_attributes=True) for ras in access_model]
            return access_schema


###ROLE ACCESS MANAGER
class DataRoleAccessManager:
    @classmethod
    async def add_access_with_session(cls, data: SDataRoleAccessAdd, session):
        access_dict = data.model_dump()
        access = DataRoleAccessOrm(**access_dict)
        session.add(access)
        await session.flush()

    @classmethod
    async def add_access(cls, data: SDataRoleAccessAdd):
        async with session_factory() as session:
            access_dict = data.model_dump()
            access = DataRoleAccessOrm(**access_dict)
            session.add(access)
            await session.flush()
            await session.commit()

    @classmethod
    async def read_access_all(cls):
        async with session_factory() as session:
            query = select(DataRoleAccessOrm)
            result = await session.execute(query)
            access_model = result.scalars().all()
            return access_model


###DATA ACCESS MANAGER
user_access_manager = DataUserAccessManager()
role_access_manager = DataRoleAccessManager()


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
    async def read_data_my(cls, user_id: int):
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
