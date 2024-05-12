from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.configuration.database import delete_tables, create_tables
from server.user.router import router as user_router
from server.role.router import router as role_router
from server.data.router import router as data_router


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
    prefix="/user",
    tags=["User"],
)

app.include_router(
    role_router,
    prefix="/role",
    tags=["Role"],
)

app.include_router(
    data_router,
    prefix="/data",
    tags=["Data"],
)


@app.get("/")
def hello():
    return {"message": "Hello World!"}
