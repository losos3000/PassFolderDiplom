from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi_users import fastapi_users, FastAPIUsers

from auth import auth_backend
from database.db_connect import delete_tables, create_tables, User
from manager import get_user_manager
from models.schemas import UserRead, UserCreate
from routers import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print("INFO: [db]: База очищена")
    # await create_tables()
    print("INFO: [db]: База готова")
    yield
    print("INFO: Выключение")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI(
    lifespan=lifespan,
    title="DataSec",
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/db",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    user_router.router,
    prefix="/user",
    tags=["User"],
)


@app.get("/")
def hello():
    return {"message": "HelloWorld!"}
