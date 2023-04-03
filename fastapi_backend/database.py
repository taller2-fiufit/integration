import os
import time
from typing import Any, Optional
import psycopg as pg
from psycopg.rows import class_row
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
    conn: Optional[pg.Connection[Any]]

    def __init__(
        self, connection: Optional[pg.Connection[Any]] = None
    ) -> None:
        self.conn = connection if connection is not None else self._connect()
        self._init_tables()

    def _connect(self) -> pg.Connection[Any]:
        # NOTE: mypy fails without the first parameter
        conninfo = make_conninfo("", **DB_KWARGS)
        print(conninfo)

        while True:
            try:
                return pg.connect(
                    conninfo,
                    autocommit=True,
                )
            except pg.OperationalError:
                time.sleep(2)
                continue

    def _init_tables(self) -> None:
        assert self.conn is not None
        try:
            with self.conn.cursor() as cur:
                query = """CREATE TABLE msg
                    (
                        id INT PRIMARY KEY NOT NULL,
                        msg TEXT NOT NULL
                    );"""
                cur.execute(query)
        except pg.Error as e:
            print(e)

    def get_msg(self) -> Optional["Message"]:
        assert self.conn is not None
        with self.conn.cursor(row_factory=class_row(Message)) as cur:
            query = "SELECT msg FROM msg WHERE id = 0;"
            cur.execute(query)
            msg: Optional[Message] = cur.fetchone()

        return msg

    def put_msg(self, msg: "Message") -> None:
        assert self.conn is not None
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
