from typing import List

from fastapi import HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy import select, delete, update

from server.configuration.database import session_factory

from server.data.acccess.manager import user_access_manager
from server.data.acccess.models import DataUserAccessOrm
from server.data.acccess.schemas import SDataUserAccessAdd, SDataUserAccessRead
from server.data.models import DataOrm
from server.data.schemas import SDataAdd, SDataRead, SDataGet, SDataWithAccessRead, SDataEdit, SData

from server.user.models import UserOrm

data_ta = TypeAdapter(List[SDataRead])


def response_validate(data) -> List[SDataRead]:
    result = [SDataRead.model_validate(d, from_attributes=True) for d in data]
    return result


class DataManager:
    @classmethod
    async def add_data(
            cls,
            user: UserOrm,
            data: SDataAdd,
    ):
        async with session_factory() as session:
            ds_data_dict = data.model_dump()
            ds_data = DataOrm(**ds_data_dict)
            session.add(ds_data)
            await session.flush()

            if user.is_superuser is not True:
                user_access = SDataUserAccessAdd(
                    ds_data_id=ds_data.id,
                    ds_user_id=user.id,
                    access_read=True,
                    access_edit=True,
                )
                await user_access_manager.add_access(
                    session=session,
                    data=user_access,
                )

            await session.commit()

    @classmethod
    async def read_data(
            cls,
            user: UserOrm,
            data: SDataGet,
    ) -> List[SDataWithAccessRead]:
        async with session_factory() as session:
            if data.id is not None:
                _access: List[SDataUserAccessRead] = await user_access_manager.read_access(
                    session=session,
                    user_id=user.id,
                    data_id=data.id,
                )
                access: SDataUserAccessRead  = _access[0]
                if user.is_superuser or access.access_read:
                    query = select(DataOrm).where(DataOrm.id == data.id)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="FORBIDDEN",
                    )
            elif data.id is None:
                print("AAAAAAAAAAAAAAAAAAAAa")
                if user.is_superuser:
                    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBb")
                    query = select(DataOrm)
                else:
                    print("CCCCCCCCCCCCCCCCCCCCCCC")
                    query = (
                        select(DataOrm)
                        .join(
                            DataUserAccessOrm,
                            DataUserAccessOrm.ds_data_id == DataOrm.id
                        ).filter(
                            DataUserAccessOrm.ds_user_id == user.id
                        ).filter(
                            DataUserAccessOrm.access_read == True
                        )
                    )
                    print(query)
            result = await session.execute(query)
            ds_data_model = result.scalars().all()
            ds_data_schema: List[SDataRead] = response_validate(ds_data_model)

            ds_data_with_access: List[SDataWithAccessRead] = []

            for i in range(0, len(ds_data_schema), 1):
                access = await user_access_manager.read_access(
                    session=session,
                    data_id=ds_data_schema[i].id
                )
                temp = SDataWithAccessRead(
                    id=ds_data_schema[i].id,
                    name=ds_data_schema[i].name,
                    login=ds_data_schema[i].login,
                    password=ds_data_schema[i].password,
                    url=ds_data_schema[i].url,
                    description=ds_data_schema[i].description,
                    access=access,
                )
                ds_data_with_access.append(temp)

            return ds_data_with_access

    @classmethod
    async def delete_data(cls, data_id, user: UserOrm):
        async with session_factory() as session:
            _access: List[SDataUserAccessRead] = await user_access_manager.read_access(
                session=session,
                data_id=data_id,
                user_id=user.id,
            )
            access: SDataUserAccessRead = _access[0]
            print(access)
            if user.is_superuser is False and access.access_edit is False:
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

    @classmethod
    async def edit_data(
            cls,
            user: UserOrm,
            new_data: SDataEdit,
    ):
        async with session_factory() as session:
            _access: List[SDataUserAccessRead] = await user_access_manager.read_access(
                session=session,
                data_id=new_data.id,
                user_id=user.id,
            )
            access = _access[0]

            if user.is_superuser or access.access_edit:
                try:
                    if new_data.name is not None:
                        name_query = update(DataOrm).values(name=new_data.name).filter(DataOrm.id == new_data.id)
                        await session.execute(name_query)
                    if new_data.login is not None:
                        login_query = update(DataOrm).values(login=new_data.login).filter(DataOrm.id == new_data.id)
                        await session.execute(login_query)
                    if new_data.password is not None:
                        password_query = update(DataOrm).values(password=new_data.password).filter(DataOrm.id == new_data.id)
                        await session.execute(password_query)
                    if new_data.url is not None:
                        url_query = update(DataOrm).values(url=new_data.url).filter(DataOrm.id == new_data.id)
                        await session.execute(url_query)
                    if new_data.description is not None:
                        description_query = update(DataOrm).values(description=new_data.description).filter(DataOrm.id == new_data.id)
                        await session.execute(description_query)

                    if len(new_data.access) > 0:
                        await user_access_manager.delete_access(
                            session=session,
                            data_id=new_data.id,
                            author_id=user.id,
                        )
                        for i in range(0, len(new_data.access), 1):
                            if new_data.access[i].ds_user_id == user.id:
                                continue
                            new_access = SDataUserAccessAdd(
                                ds_data_id=new_data.id,
                                ds_user_id=new_data.access[i].ds_user_id,
                                access_read=new_data.access[i].access_read,
                                access_edit=new_data.access[i].access_edit,
                            )
                            await user_access_manager.add_access(
                                session=session,
                                data=new_access
                            )

                    await session.flush()
                    await session.commit()

                except HTTPException as e:
                    raise HTTPException(
                        status_code=e.status_code,
                        detail=e.detail
                    )
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="INTERNAL SERVER ERROR"
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Отказано в доступе"
                )


data_manager = DataManager()
