from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from fastapi import Depends, FastAPI
from fastapi_backend.database import Database, Message
from fastapi.middleware.cors import CORSMiddleware


async def get_db() -> Database:
    if not hasattr(get_db, "db_conn"):
        get_db.db_conn = Database()  # type: ignore[attr-defined]

    return get_db.db_conn  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # warmup database
    await get_db()
    yield


app = FastAPI(lifespan=lifespan, dependencies=[Depends(get_db)])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_msg(db: Annotated[Database, Depends(get_db)]) -> Message:
    msg = db.get_msg()
    return msg if msg is not None else Message()


@app.put("/")
async def put_msg(
    rcvd_msg: Message, db: Annotated[Database, Depends(get_db)]
) -> None:
    db.put_msg(rcvd_msg)
