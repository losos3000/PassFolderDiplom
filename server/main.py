from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

# from server.configuration.database import delete_tables, create_table

from server.user.router import router as user_router
from server.data.router import router as data_router
# from server.data.acccess.router import router as access_router
# from client.pages.router import router as pages_router

from server.reset import reset


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await reset()
    yield
    print("INFO:    Выключение")


app = FastAPI(
    lifespan=lifespan,
    title="DataSec",
)

origins = [
    "localhost",
    "localhost:8080",
    "127.0.0.1:8080",
    "127.0.0.1",
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

# app.include_router(
#     access_router,
#     prefix="/access",
#     tags=["Access"],
# )

# app.include_router(
#     pages_router,
#     tags=["Page"],
# )