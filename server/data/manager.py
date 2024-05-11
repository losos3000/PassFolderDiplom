from sqlalchemy import select

from server.configuration.database import session_factory
from server.data.models import DataOrm
from server.data.schemas import SDataAdd


class DataManager:
    @classmethod
    async def add_data(cls, data: SDataAdd) -> int:
        async with session_factory() as session:
            ds_data_dict = data.model_dump()
            ds_data = DataOrm(**ds_data_dict)
            session.add(ds_data)
            await session.flush()
            await session.commit()
            return ds_data.id

    @classmethod
    async def read_data_all(cls):
        async with session_factory() as session:
            query = select(DataOrm)
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            return ds_data_model
