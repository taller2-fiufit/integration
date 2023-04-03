from typing import Any
import psycopg as pg


def test_database_init(postgresql: pg.Connection[Any]) -> None:
    with postgresql.cursor() as cur:
        cur.execute("SELECT version();")
        cur.fetchone()
