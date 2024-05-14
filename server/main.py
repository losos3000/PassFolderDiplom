from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.configuration.database import delete_tables, create_tables
from server.user.router import router as user_router
from server.role.router import router as role_router
from server.data.router import router as data_router

from client.pages.router import router as pages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print("INFO: [db]: База очищена")
    # await create_tables()
    # print("INFO: [db]: База готова")
    yield
    print("INFO: Выключение")


app = FastAPI(
    lifespan=lifespan,
    title="DataSec",
)

app.include_router(
    user_router,
    prefix="/api/user",
    tags=["User"],
)

app.include_router(
    role_router,
    prefix="/api/role",
    tags=["Role"],
)

app.include_router(
    data_router,
    prefix="/api/data",
    tags=["Data"],
)

app.include_router(
    pages_router,
    tags=["Pages"],
)
