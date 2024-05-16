from typing import Optional

from fastapi import Depends, Request

from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable, SQLAlchemyAccessTokenDatabase

from sqlalchemy import ForeignKey, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from server.configuration.basemodel import Base
from server.configuration.config import settings
from server.configuration.database import get_async_session, session_factory
from server.role.models import RoleOrm
from server.role.schemas import SRoleRead
from server.user.models import UserOrm, RoleToUserOrm
from server.user.schemas import SRoleToUserRead, SUserRead, SRoleToUserAdd

SECRET = settings.AUTH_SECRET


class UserRoleManager:

    @classmethod
    async def add_user_role(cls, data: SRoleToUserAdd):
        async with session_factory() as session:
            role_dict = data.model_dump()
            role = RoleToUserOrm(**role_dict)
            session.add(role)
            await session.flush()
            await session.commit()


class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserOrm, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # async def on_after_forgot_password(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     print(f"User {user.id} has forgot their password. Reset token: {token}")
    #
    # async def on_after_request_verify(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     print(f"Verification requested for user {user.id}. Verification token: {token}")

    @classmethod
    async def read_user_me(cls, user_id: int):
        async with session_factory() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            user_model = result.scalars().all()
            return user_model

    @classmethod
    async def read_user_all(cls):
        async with session_factory() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_model = result.scalars().all()
            user_schema = [SUserRead.model_validate(um, from_attributes=True) for um in user_model]
            return user_schema

    @classmethod
    async def read_user_role_me(cls, user_id: int):
        async with session_factory() as session:
            query = (
                select(RoleOrm)
                .join(
                    RoleToUserOrm,
                    RoleToUserOrm.ds_role_id == RoleOrm.id,
                ).filter(
                    RoleToUserOrm.ds_user_id == user_id,
                )
            )
            result = await session.execute(query)
            role_model = result.scalars().all()
            role_schema = [SRoleRead.model_validate(rm, from_attributes=True) for rm in role_model]
            return role_schema

    @classmethod
    async def read_user_role_all(cls):
        async with session_factory() as session:
            query = select(RoleToUserOrm)
            result = await session.execute(query)
            user_role_model = result.scalars().all()
            user_role_schema = [SRoleToUserRead.model_validate(urm, from_attributes=True) for urm in user_role_model]
            return user_role_schema


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    @declared_attr
    def user_id(self) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("ds_user.id", ondelete="cascade"), nullable=False)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserOrm)


cookie_transport = CookieTransport(cookie_name="user", cookie_max_age=3600)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="db",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)


fastapi_users = FastAPIUsers[UserOrm, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user()
