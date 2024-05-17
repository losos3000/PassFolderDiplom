from typing import List

from fastapi import HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy import select, delete

from server.configuration.database import session_factory

from server.data.acccess.manager import user_access_manager
from server.data.acccess.models import DataUserAccessOrm
from server.data.acccess.schemas import SDataUserAccessAdd, SDataUserAccessRead

from server.data.models import DataOrm
from server.data.schemas import SDataAdd, SDataRead, SDataGet
from server.user.models import UserOrm

data_ta = TypeAdapter(List[SDataRead])


def response_validate(data) -> List[SDataRead]:
    result = [SDataRead.model_validate(d, from_attributes=True) for d in data]
    return result


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
            await user_access_manager.add_access(
                session=session,
                data=user_access,
            )

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
    async def read_data(
            cls,
            user: UserOrm,
            data: SDataGet,
    ):
        async with session_factory() as session:
            if data.id is not None:
                access: SDataUserAccessRead = user_access_manager.read_access(
                    session=session,
                    user_id=user.id,
                    data_id=data.id,
                )[0]
                if user.is_superuser or access.access_read:
                    query = select(DataOrm).where(DataOrm.id == data.id)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="FORBIDDEN",
                    )
            elif data.id is None:
                if user.is_superuser:
                    query = select(DataOrm)
                else:
                    query = (
                        select(DataOrm)
                        .join(
                            DataUserAccessOrm,
                            DataUserAccessOrm.ds_data_id == DataOrm.id,
                        ).filter(
                            DataUserAccessOrm.ds_user_id == user.id,
                        )
                    )
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            ds_data_schema: List[SDataRead] = [SDataRead.model_validate(ddm, from_attributes=True) for ddm in ds_data_model]

            for i in range(0, len(ds_data_schema), 1):
                ds_data_schema[i].access = user_access_manager(
                    session=session,
                    data_id=ds_data_schema[i].id
                )
            return ds_data_schema

    @classmethod
    async def delete_data(cls, data_id, user: UserOrm):
        async with session_factory() as session:
            access: List[SDataUserAccessRead] = user_access_manager.read_access(
                session=session,
                data_id=data_id,
                user_id=user.id,
            )
            if user.is_superuser is False and access[0].access_edit is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Отказано в доступе"
                )
            try:
                del_access = delete(DataUserAccessOrm).where(DataUserAccessOrm.ds_data_id == data_id)
                await session.execute(del_access)
                del_data = delete(DataOrm).where(DataOrm.id == data_id)
                await session.execute(del_data)
                await session.flush()
                await session.commit()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="INTERNAL SERVER ERROR"
                )


data_manager = DataManager()
