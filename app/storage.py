"""Where items are kept: in memory (tests, quick runs) or in PostgreSQL (Compose)."""

import psycopg
from psycopg.rows import dict_row


class MemoryStorage:
    """Items live in a dict and are lost when the app stops."""

    def __init__(self) -> None:
        self.items: dict[int, dict] = {}

    def list_items(self) -> list[dict]:
        """Return every item."""
        return list(self.items.values())

    def create_item(self, name: str, price: float) -> dict:
        """Store a new item and give it the next id."""
        new_id = len(self.items) + 1
        item = {"id": new_id, "name": name, "price": price}
        self.items[new_id] = item
        return item

    def get_item(self, item_id: int) -> dict | None:
        """Return one item, or None if it does not exist."""
        return self.items.get(item_id)

    def clear(self) -> None:
        """Forget every item (used by the tests)."""
        self.items.clear()


class PostgresStorage:  # pragma: no cover
    """Items live in a PostgreSQL table and survive restarts."""

    def __init__(self, url: str) -> None:
        self.url = url
        # Connect once at startup and create the table if it is missing.
        # If the database is not reachable, the app stops here.
        with psycopg.connect(self.url) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS items ("
                "id SERIAL PRIMARY KEY, "
                "name TEXT NOT NULL, "
                "price DOUBLE PRECISION NOT NULL)"
            )

    def list_items(self) -> list[dict]:
        """Return every item."""
        with psycopg.connect(self.url, row_factory=dict_row) as conn:
            return conn.execute(
                "SELECT id, name, price FROM items ORDER BY id"
            ).fetchall()

    def create_item(self, name: str, price: float) -> dict:
        """Store a new item; PostgreSQL chooses the id."""
        with psycopg.connect(self.url, row_factory=dict_row) as conn:
            return conn.execute(
                "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id, name, price",
                (name, price),
            ).fetchone()

    def get_item(self, item_id: int) -> dict | None:
        """Return one item, or None if it does not exist."""
        with psycopg.connect(self.url, row_factory=dict_row) as conn:
            return conn.execute(
                "SELECT id, name, price FROM items WHERE id = %s", (item_id,)
            ).fetchone()
