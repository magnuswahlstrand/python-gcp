from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    resp = client.post("/", json={"user": "Magnus"})
    assert resp.status_code == 200, resp.json()
    assert resp.json() == {"user": "Magnus"}


def test_read_main2():
    response = client.post("/")
    assert response.status_code == 422
