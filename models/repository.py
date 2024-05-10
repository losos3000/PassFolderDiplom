from sqlalchemy import select
from database.db_connect import session_factory, User


# from models.models import UserOrm, RoleOrm
# from models.schemas import SUserAdd, SRoleAdd


class UserRepository:
#     @classmethod
#     async def add_user(cls, data: SUserAdd) -> int:
#         async with session_factory() as session:
#             user_dict = data.model_dump()
#             user = UserOrm(**user_dict)
#             session.add(user)
#             await session.flush()
#             await session.commit()
#             return user.id
#
    @classmethod
    async def read_user_all(cls):
        async with session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            user_model = result.scalars().all()
            return user_model


# class RoleRepository:
#     @classmethod
#     async def add_role(cls, data: SRoleAdd) -> int:
#         async with session_factory() as session:
#             role_dict = data.model_dump()
#             role = RoleOrm(**role_dict)
#             session.add(role)
#             await session.flush()
#             await session.commit()
#             return role.id
#
#     @classmethod
#     async def read_role_all(cls):
#         async with session_factory() as session:
#             query = select(RoleOrm)
#             result = await session.execute(query)
#             role_model = result.scalars().all()
#             return role_model


# class AuthTest:
#     @classmethod
#     async def get_user_db(cls: AsyncSession = Depends(get_async_session)):
#         yield SQLAlchemyUserDatabase(cls, UserOrm)
