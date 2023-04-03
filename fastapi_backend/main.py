from typing import Optional
from fastapi import FastAPI
from fastapi_backend.database import Database, Message
from fastapi.middleware.cors import CORSMiddleware


db = Database()


def setup() -> None:
    db.init()


app = FastAPI(on_startup=[setup])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_msg() -> Message:
    msg = db.get_msg()
    return msg if msg is not None else Message()


@app.put("/")
async def put_msg(rcvd_msg: Message) -> None:
    db.put_msg(rcvd_msg)
