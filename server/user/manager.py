from typing import Optional, List

from fastapi import Depends, Request

from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers, exceptions, models
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.password import PasswordHelperProtocol, PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable, SQLAlchemyAccessTokenDatabase

from sqlalchemy import ForeignKey, Integer, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from cipher.cipher import cipher_manager

from server.configuration.basemodel import Base
from server.configuration.config import settings
from server.configuration.database import get_async_session, session_factory
from server.data.acccess.manager import user_access_manager
from server.user.models import UserOrm
from server.user.schemas import SUserRead, SUserDelete, SUserAdd, SUserEdit, SUserAuth, SUser

SECRET = settings.AUTH_SECRET
password_helper: PasswordHelperProtocol = PasswordHelper()


def response_validate(data) -> List[SUserRead]:
    result = [SUserRead.model_validate(d, from_attributes=True) for d in data]
    return result


###USER MANAGER
class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    @classmethod
    async def edit_user(cls, data: SUserEdit):
        async with session_factory() as session:
            new_user_dict = data.model_dump()
            password = new_user_dict.pop("password")
            new_user_dict["hashed_password"] = password
            new_user = UserOrm(**new_user_dict)

            if new_user.email is not None:
                email_query = update(UserOrm).values(email=new_user.email).filter(UserOrm.id == new_user.id)
                await session.execute(email_query)
            if new_user.name is not None:
                name_query = update(UserOrm).values(name=new_user.name).filter(UserOrm.id == new_user.id)
                await session.execute(name_query)
            if new_user.hashed_password is not None:
                new_password = password_helper.hash(new_user.hashed_password)
                pass_query = update(UserOrm).values(hashed_password=new_password).filter(UserOrm.id == new_user.id)
                await session.execute(pass_query)
            if new_user.is_superuser is not None:
                super_query = update(UserOrm).values(is_superuser=new_user.is_superuser).filter(UserOrm.id == new_user.id)
                await session.execute(super_query)

            await session.flush()
            await session.commit()

    @classmethod
    async def read_user(cls, user_id: int):
        async with session_factory() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            user_model = result.scalars().all()
            user_schema = response_validate(user_model)
            return user_schema

    @classmethod
    async def read_user_all(cls):
        async with session_factory() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_model = result.scalars().all()
            user_schema = response_validate(user_model)
            return user_schema

    @classmethod
    async def delete_user(cls, data: SUserDelete):
        async with session_factory() as session:
            await user_access_manager.delete_access(
                session=session,
                user_id=data.id,
            )
            await session.execute(delete(AccessToken).where(AccessToken.user_id == data.id))
            query = delete(UserOrm).where(UserOrm.id == data.id)
            await session.execute(query)
            await session.flush()
            await session.commit()


###OTHER
class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    @declared_attr
    def user_id(self) -> Mapped[int]:
        return mapped_column(Integer, ForeignKey("ds_user.id", ondelete="cascade"), nullable=False)


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserOrm)


cookie_transport = CookieTransport(
    cookie_name="user",
    cookie_max_age=3600,
    # cookie_secure=True,   
    # cookie_samesite="strict",
    cookie_httponly=False,
    cookie_path="/",
    # cookie_domain="127.0.0.1"
)


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
current_superuser = fastapi_users.current_user(active=True, superuser=True)