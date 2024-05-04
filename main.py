from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("INFO: [db]: База очищена")
    await create_tables()
    print("INFO: [db]: База готова")
    yield
    print("INFO: Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


@app.get("/")
def hello():
    return {"message": "Hello!"}
