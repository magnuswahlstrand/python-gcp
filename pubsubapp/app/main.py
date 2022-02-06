import base64
import json
import os

import sentry_sdk
from fastapi import FastAPI
from fastapi.logger import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .models import PubSubEnvelope, OrderCreatedEvent, OrderFulfilledEvent

app = FastAPI()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_CONNECTION_STRING", ""),
    environment=os.getenv('ENV', 'dev'),  # You should read it from environment variable
    traces_sample_rate=1.0
)

try:
    app.add_middleware(SentryAsgiMiddleware)
except Exception as e:
    logger.error("failed to setup sentry middleware", e)
    # pass silently if the Sentry integration failed
    pass


def unpack_pubsub_message(envelope: PubSubEnvelope) -> dict:
    logger.info("unpack", event=envelope)
    print("unpack 2", envelope)
    return json.loads(base64.b64decode(envelope.message.data))


# {"id": "d5922279-3708-4202-aec0-4dacb92ebd2f", "user_id": "af283697-fcb3-4ba2-8d0e-7338eaf5a265"}


@app.post("/order/created")
async def order_created(pubsub_message: PubSubEnvelope):
    event = OrderCreatedEvent(**unpack_pubsub_message(pubsub_message))
    logger.info("order created", event=event)
    print("order created 2", event)
    return {'id': event.id}


@app.post("/order/fulfilled")
async def order_fulfilled(pubsub_message: PubSubEnvelope):
    event = OrderFulfilledEvent(**unpack_pubsub_message(pubsub_message))
    logger.info("order fulfilled", event=event)
    print("order fulfilled 2", event)
    return {'id': event.id}
