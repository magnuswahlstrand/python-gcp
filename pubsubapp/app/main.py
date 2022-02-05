from typing import Optional

from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseModel

app = FastAPI()


class UserIn(BaseModel):
    user: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def read_root(user_in: UserIn):
    logger.info("Got a request", user=user_in)
    return user_in


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
