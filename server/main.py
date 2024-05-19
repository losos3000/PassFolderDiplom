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
    "localhost:8080",
    "127.0.0.1:8080",
    "localhost:5173",
    "127.0.0.1:5173",
    "http://localhost:5173/",
    "http://127.0.0.1:5173/",
    "http://localhost:5173/login",
    "http://127.0.0.1:5173/login",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*", "'Access-Control-Allow-Origin'"],
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
