from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import os, time
import psycopg2


def setup():
    global conn
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host=os.environ.get("POSTGRES_SERVICE_HOST"),
                port=os.environ.get("POSTGRES_SERVICE_PORT"),
            )
            break
        except psycopg2.OperationalError:
            time.sleep(2)
            continue

    with conn.cursor() as cur:
        query = "CREATE TABLE msg (id INT PRIMARY KEY NOT NULL, msg TEXT NOT NULL);"
        cur.execute(query)


app = FastAPI(on_startup=[setup])

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
    msg = ""

    with conn.cursor() as cur:
        query = "SELECT msg FROM msg WHERE id = 0;"
        cur.execute(query)
        msg = cur.fetchall()

    return msg


@app.put("/")
async def root(rcvd_msg: Message):
    with conn.cursor() as cur:
        query = f"""
            INSERT INTO msg
            VALUES(0, '{rcvd_msg.msg}')
            ON CONFLICT(id)
            DO UPDATE SET msg = EXCLUDED.msg;
        """
        cur.execute(query)

