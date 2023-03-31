import os
import time
from typing import Any, Optional
import psycopg
from psycopg.conninfo import make_conninfo
from pydantic import BaseModel

DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_SERVICE_HOST")
DB_PORT = os.environ.get("POSTGRES_SERVICE_PORT")

DB_KWARGS = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST,
    "port": DB_PORT,
}


class Database:
    conn: psycopg.Connection[Any]

    def connect(self) -> None:
        conninfo = make_conninfo(kwargs=DB_KWARGS)
        print(conninfo)

        while True:
            try:
                self.conn = psycopg.connect(
                    conninfo,
                    autocommit=True,
                )
                break
            except psycopg.OperationalError:
                time.sleep(2)
                continue

        self.init_tables()

    def init_tables(self) -> None:
        try:
            with self.conn.cursor() as cur:
                query = """CREATE TABLE msg
                    (
                        id INT PRIMARY KEY NOT NULL,
                        msg TEXT NOT NULL
                    );"""
                cur.execute(query)
        except psycopg.Error as e:
            print(e)

    def get_msg(self) -> Optional["Message"]:
        with self.conn.cursor() as cur:
            query = "SELECT msg FROM msg WHERE id = 0;"
            cur.execute(query)
            msg: Optional[Message] = cur.fetchone()

        return msg

    def put_msg(self, msg: "Message") -> None:
        with self.conn.cursor() as cur:
            query = """
                INSERT INTO msg
                VALUES(0, %s)
                ON CONFLICT(id)
                DO UPDATE SET msg = EXCLUDED.msg;
            """
            cur.execute(query, [msg])


class Message(BaseModel):
    msg: str = ""
