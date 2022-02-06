from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PubSubPayload(BaseModel):
    attributes: Optional[dict]
    data: str


class PubSubEnvelope(BaseModel):
    message: PubSubPayload


class BaseEvent(BaseModel):
    id: UUID
    user_id: UUID


class OrderCreatedEvent(BaseEvent):
    pass


class OrderFulfilledEvent(BaseEvent):
    pass
