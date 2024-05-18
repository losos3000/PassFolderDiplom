from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, delete

from server.data.acccess.models import DataUserAccessOrm
from server.data.acccess.schemas import SDataUserAccessAdd, SDataUserAccessRead


def response_validate(data) -> List[SDataUserAccessRead]:
    result = [SDataUserAccessRead.model_validate(d, from_attributes=True) for d in data]
    return result


class DataUserAccessManager:
    @classmethod
    async def add_access(
            cls,
            session,
            data: SDataUserAccessAdd
    ):
        access_dict = data.model_dump()
        access = DataUserAccessOrm(**access_dict)
        session.add(access)
        await session.flush()

    @classmethod
    async def read_access(
            cls,
            session,
            data_id: int | None = None,
            user_id: int | None = None
    ) -> List[SDataUserAccessRead]:

        if data_id is None and user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Даннные для чтения не указаны"
            )
        elif data_id is not None and user_id is None:
            query = select(DataUserAccessOrm).where(
                DataUserAccessOrm.ds_data_id == data_id
            )
        elif data_id is None and user_id is not None:
            query = select(DataUserAccessOrm).where(
                DataUserAccessOrm.ds_user_id == user_id
            )
        elif data_id is not None and user_id is not None:
            query = select(DataUserAccessOrm).where(
                DataUserAccessOrm.ds_data_id == data_id
            ).where(
                DataUserAccessOrm.ds_user_id == user_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Данные для чтения указаны некорректно"
            )

        result = await session.execute(query)
        access_model = result.scalars().all()
        access_schema = response_validate(access_model)
        return access_schema

    @classmethod
    async def delete_access(
            cls,
            session,
            data_id: int | None = None,
            user_id: int | None = None,
            author_id: int | None = None,
    ):

        if data_id is None and user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не указаны даннные для удаления"
            )
        elif data_id is not None and user_id is None:
            query = delete(DataUserAccessOrm).where(
                DataUserAccessOrm.ds_data_id == data_id
            ).where(
                DataUserAccessOrm.ds_user_id != author_id
            )
        elif data_id is None and user_id is not None:
            query = delete(DataUserAccessOrm).where(
                DataUserAccessOrm.ds_user_id == user_id
            ).where(
                DataUserAccessOrm.ds_user_id != author_id
            )
        elif data_id is not None and user_id is not None:
            query = delete(DataUserAccessOrm).where(
                DataUserAccessOrm.ds_data_id == data_id
            ).where(
                DataUserAccessOrm.ds_user_id == user_id
            ).where(
                DataUserAccessOrm.ds_user_id != author_id
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Данные для удаления указаны некорректно"
            )

        await session.execute(query)
        await session.flush()


user_access_manager = DataUserAccessManager()
