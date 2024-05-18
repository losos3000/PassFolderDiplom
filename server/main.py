from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from server.user.router import router as user_router
from server.data.router import router as data_router

from server.reset import reset


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO:     [system] Включение")
    # await reset()
    yield
    print("INFO:     [system] Выключение")


app = FastAPI(
    lifespan=lifespan,
    title="DataSec",
)

origins = [
    "localhost",
    "localhost:8080",
    "127.0.0.1:8080",
    "127.0.0.1",
    "192.168.0.2:8000",
    "192.168.0.2",
    "192.168.0.6",
    "192.168.0.6:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user_router,
    prefix="/api/user",
    tags=["User"],
)

app.include_router(
    data_router,
    prefix="/api/data",
    tags=["Data"],
)
