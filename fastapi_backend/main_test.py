from fastapi_backend.database import Database
from .main import app, get_db
from typing import Any
from fastapi.testclient import TestClient
import psycopg as pg
from .database import Message


def setup_subjects(connection: pg.Connection[Any]) -> TestClient:
    db = Database(connection)

    def get_mock_db() -> Database:
        return db

    # https://fastapi.tiangolo.com/advanced/testing-dependencies/
    app.dependency_overrides[get_db] = get_mock_db

    return TestClient(app)


def test_app_get_empty(postgresql: pg.Connection[Any]) -> None:
    client = setup_subjects(postgresql)

    response = client.get("/")

    assert response.status_code == 200

    json = response.json()

    assert json["msg"] == ""


def test_app_put(postgresql: pg.Connection[Any]) -> None:
    client = setup_subjects(postgresql)

    body = Message(msg="tuki")

    response = client.put("/", json=body.dict())

    assert response.status_code == 200


def test_app_put_get(postgresql: pg.Connection[Any]) -> None:
    client = setup_subjects(postgresql)

    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["msg"] == ""

    body = Message(msg="tuki")
    response = client.put("/", json=body.dict())
    assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["msg"] == "tuki"
