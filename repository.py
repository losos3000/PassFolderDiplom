from sqlalchemy import select

from database import new_session, UserOrm
from schemas import SUserAdd


class UserRepository():
    @classmethod
    async def add_user(cls, data: SUserAdd) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UserOrm(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id


    @classmethod
    async def show_all_users(cls):
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_models = result.scalars().all()
            return user_models
