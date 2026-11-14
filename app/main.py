"""A small API used to learn DevOps: every later tool will build, test, deploy and watch it."""

import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.storage import MemoryStorage, PostgresStorage

APP_VERSION = "1.0.0"

app = FastAPI(title="devops-app", version=APP_VERSION)


class ItemIn(BaseModel):
    """What a client must send to create an item."""

    name: str
    price: float


class Item(ItemIn):
    """What the API returns: the item plus its id."""

    id: int


# Where items are kept. With DATABASE_URL set (Compose), a real PostgreSQL database.
# Without it (tests, quick runs), a simple dict in memory.
DATABASE_URL = os.environ.get("DATABASE_URL")
storage = PostgresStorage(DATABASE_URL) if DATABASE_URL else MemoryStorage()


@app.get("/health")
def health() -> dict:
    """Liveness check used by Kubernetes, monitoring and CI."""
    return {"status": "ok", "version": APP_VERSION}


@app.get("/items")
def list_items() -> list[Item]:
    """Return every item."""
    return storage.list_items()


@app.post("/items", status_code=201)
def create_item(item: ItemIn) -> Item:
    """Create an item and give it the next id."""
    return storage.create_item(item.name, item.price)


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    """Return one item, or 404 if it does not exist."""
    found = storage.get_item(item_id)
    if found is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return found
