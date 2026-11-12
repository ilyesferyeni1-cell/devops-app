"""A small API used to learn DevOps: every later tool will build, test, deploy and watch it."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

APP_VERSION = "1.0.0"

app = FastAPI(title="devops-app", version=APP_VERSION)


class ItemIn(BaseModel):
    """What a client must send to create an item."""

    name: str
    price: float


class Item(ItemIn):
    """What the API returns: the item plus its id."""

    id: int


# In-memory "database": a simple dict that is lost when the app stops.
# (A real database arrives with Docker Compose in Step 4.2.)
items: dict[int, Item] = {}


@app.get("/health")
def health() -> dict:
    """Liveness check used by Kubernetes, monitoring and CI."""
    return {"status": "ok", "version": APP_VERSION}


@app.get("/items")
def list_items() -> list[Item]:
    """Return every item."""
    return list(items.values())


@app.post("/items", status_code=201)
def create_item(item: ItemIn) -> Item:
    """Create an item and give it the next id."""
    new_id = len(items) + 1
    created = Item(id=new_id, **item.model_dump())
    items[new_id] = created
    return created


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    """Return one item, or 404 if it does not exist."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
