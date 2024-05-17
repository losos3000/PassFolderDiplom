import asyncio

from server.configuration import settings
from server.configuration.database import delete_tables, create_tables, session_factory
from server.user.manager import UserManager
from server.user.models import UserOrm
from server.user.schemas import SUserAdd, SUser
from fastapi_users.password import PasswordHelperProtocol, PasswordHelper

password_helper: PasswordHelperProtocol = PasswordHelper()


async def register_superuser():
    superuser_data = SUser(
        id=0,
        email=settings.SUPERUSER_EMAIL,
        hashed_password=settings.SUPERUSER_PASSWORD,
        name=settings.SUPERUSER_NAME,
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )
    async with session_factory() as session:
        new_user_dict = superuser_data.model_dump()
        new_user = UserOrm(**new_user_dict)
        password = new_user.hashed_password
        new_user.hashed_password = password_helper.hash(password)
        session.add(new_user)
        await session.flush()
        await session.commit()




async def reset():
    await delete_tables()
    print("INFO:    [db]: База очищена")
    await create_tables()
    print("INFO:    [db]: База готова")
    await register_superuser()
    print("INFO:    [DataSec]: Суперпользователь зарегистрирован")
