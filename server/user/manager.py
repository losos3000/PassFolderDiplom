from typing import Optional, List

from fastapi import Depends, Request

from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers, exceptions, models
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.password import PasswordHelperProtocol
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable, SQLAlchemyAccessTokenDatabase

from sqlalchemy import ForeignKey, Integer, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from cipher.cipher import cipher_manager

from server.configuration.basemodel import Base
from server.configuration.config import settings
from server.configuration.database import get_async_session, session_factory
from server.user.models import UserOrm
from server.user.schemas import SUserRead, SUserDelete, SUserAdd, SUserEdit, SUserAuth, SUser

SECRET = settings.AUTH_SECRET
password_helper: PasswordHelperProtocol


def user_validate_response(data) -> List[SUserRead]:
    result = [SUserRead.model_validate(um, from_attributes=True) for um in data]
    return result


###USER MANAGER
class UserManager(IntegerIDMixin, BaseUserManager[UserOrm, int]):

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    @classmethod
    async def add_user(cls, user_create: SUserAdd, safe: bool = False, request: Optional[Request] = None,):
        async with session_factory() as session:
            exist_user = await session.execute(select(UserOrm).where(user_create.email == UserOrm.email))

            if len((user_validate_response(exist_user))) != 0:
                raise exceptions.UserAlreadyExists()

            user_dict = (
                user_create.create_update_dict()
                if safe
                else user_create.create_update_dict_superuser()
            )
            password = user_dict.pop("password")
            user_dict["hashed_password"] = cipher_manager.hash(password)
            ds_user = UserOrm(**user_dict)

            session.add(ds_user)
            await session.flush()
            await session.commit()


    @classmethod
    async def edit_user(cls, data: SUserEdit):
        async with session_factory() as session:
            new_user_dict = data.model_dump()
            new_user = UserOrm(**new_user_dict)

            if new_user.email != "":
                email_query = update(UserOrm).values(email=new_user.email).filter(UserOrm.id==new_user.id)
            if new_user.name != "":
                name_query = update(UserOrm).values(name=new_user.name).filter(UserOrm.id == new_user.id)
            if new_user.hashed_password != "":
                print(f"PAS1 AAAAAAAAAAAAAAAA{new_user.hashed_password}")
                new_password = cipher_manager.hash(new_user.hashed_password)
                print(f"PAS2 AAAAAAAAAAAAAAAA{new_password}")
                pass_query = update(UserOrm).values(hashed_password=new_password).filter(UserOrm.id == new_user.id)

            await session.execute(email_query)
            await session.execute(name_query)
            await session.execute(pass_query)
            await session.flush()
            await session.commit()

    @classmethod
    async def read_user(cls, user_id: int):
        async with session_factory() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            user_model = result.scalars().all()
            user_schema = user_validate_response(user_model)
            return user_schema

    @classmethod
    async def read_user_all(cls):
        async with session_factory() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_model = result.scalars().all()
            user_schema = user_validate_response(user_model)
            return user_schema

    @classmethod
    async def delete_user(cls, data: SUserDelete):
        async with session_factory() as session:
            query = delete(UserOrm).where(UserOrm.id == data.id)
            await session.execute(query)
            await session.flush()
            await session.commit()

    @classmethod
    async def authenticate(cls, auth_data: SUserAuth) -> Optional[models.UP]:

        result = await session_factory().execute(select(UserOrm).where(auth_data.email == UserOrm.email))

        user_model = result.scalars().all()
        user_schema = [SUser.model_validate(um, from_attributes=True) for um in user_model]

        verified = cipher_manager.verify_pass(cipher_manager.hash(auth_data.password), user_schema[0].hashed_password)
        if not verified:
            return None

        res = models.UserProtocol
        res.id = user_schema[0].id
        res.email = user_schema[0].email
        res.hashed_password = user_schema[0].hashed_password
        res.is_active = user_schema[0].is_active
        res.is_verified = user_schema[0].is_verified
        res.is_superuser = user_schema[0].is_superuser
        return res








###OTHER
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
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user_token = fastapi_users.authenticator.current_user_token(active=True)