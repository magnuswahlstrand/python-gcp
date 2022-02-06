import base64
import json
import uuid

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from .main import app
from .models import OrderCreatedEvent, OrderFulfilledEvent

client = TestClient(app)


def dump(payload: dict):
    return {
        "message": {
            "data": base64.b64encode(json.dumps(jsonable_encoder(payload)).encode('ascii')).decode('ascii')
        }
    }


@pytest.fixture
def event_id():
    return str(uuid.uuid4())


@pytest.fixture
def user_id():
    return str(uuid.uuid4())


def test_order_created(event_id, user_id):
    event = OrderCreatedEvent(id=event_id, user_id=user_id)
    resp = client.post("/order/created", json=dump(event.dict()))
    assert resp.status_code == 200
    assert resp.json() == {"id": event_id}


def test_bad_request():
    response = client.post("/order/created", json={})
    assert response.status_code == 422


def test_order_fulfilled(event_id, user_id):
    event = OrderFulfilledEvent(id=event_id, user_id=user_id)
    resp = client.post("/order/fulfilled", json=dump(event.dict()))
    assert resp.status_code == 200
    assert resp.json() == {"id": event_id}
