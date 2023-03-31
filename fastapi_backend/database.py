import os
import time
import psycopg2
import psycopg2.extensions as ext
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
    def connect(self):
        print(DB_KWARGS)
        while True:
            try:
                self.conn = psycopg2.connect(**DB_KWARGS)
                break
            except psycopg2.OperationalError:
                time.sleep(2)
                continue

        try:
            with self.conn.cursor() as cur:
                query = (
                    "CREATE TABLE msg (id INT PRIMARY KEY NOT NULL, msg TEXT NOT NULL);"
                )
                cur.execute(query)
        except psycopg2.Error as e:
            print(e)

    def get_msg(self):
        with self.conn.cursor() as cur:
            query = "SELECT msg FROM msg WHERE id = 0;"
            cur.execute(query)
            msg = cur.fetchone()

        return msg[0] if msg is not None else None

    def put_msg(self, msg: str):
        with self.conn.cursor() as cur:
            query = f"""
                INSERT INTO msg
                VALUES(0, %s)
                ON CONFLICT(id)
                DO UPDATE SET msg = EXCLUDED.msg;
            """
            cur.execute(query, [msg])


class Message(BaseModel):
    msg = ""

    def __conform__(self, proto):
        if proto is ext.ISQLQuote:
            return self

    def getquoted(self):
        return ext.adapt(self.msg).getquoted()
