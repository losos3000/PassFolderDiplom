from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

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
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    # HTTPSRedirectMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Cookie",
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
        "Credentials",
        "X-Requested-With",
        ],
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
