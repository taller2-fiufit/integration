from fastapi import FastAPI
from fastapi_backend.database import Database, Message
from fastapi.middleware.cors import CORSMiddleware

db = Database()


def setup():
    db.connect()


app = FastAPI(on_startup=[setup])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_msg():
    return db.get_msg()


@app.put("/")
async def put_msg(rcvd_msg: Message):
    db.put_msg(rcvd_msg.msg)
