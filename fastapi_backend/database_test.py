from typing import Any
import psycopg


def test_database_init(postgresql: psycopg.Connection[Any]) -> None:
    with postgresql.cursor() as cur:
        cur.execute("SELECT version();")
        cur.fetchone()
