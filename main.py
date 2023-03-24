from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    msg = ""


msg: Message = Message()


@app.get("/")
async def root():
    global msg
    return msg


@app.put("/")
async def root(rcvd_msg: Message):
    global msg
    msg = rcvd_msg
