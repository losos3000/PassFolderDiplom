import asyncio

from server.configuration import settings
from server.configuration.database import delete_tables, create_tables
from server.user.manager import UserManager
from server.user.schemas import SUserAdd


async def register_superuser():
    superuser_data = SUserAdd(
        email=settings.SUPERUSER_EMAIL,
        password=settings.SUPERUSER_PASSWORD,
        name=settings.SUPERUSER_NAME,
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )
    await UserManager.add_user(user_create=superuser_data)


async def reset():
    await delete_tables()
    print("INFO:    [db]: База очищена")
    await create_tables()
    print("INFO:    [db]: База готова")
    await register_superuser()
    print("INFO:    [DataSec]: Суперпользователь зарегистрирован")
