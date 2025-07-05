connection_uri="put your connection URI here"

from sqlmodel import SQLModel, Field, select
from typing import Optional, List

class Item(SQLModel, table=True):
    """
    Represents an item in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offered: bool = False

from sqlmodel import create_engine, Session

engine = create_engine(connection_uri, echo=True)

from fastapi import FastAPI
from contextlib import asynccontextmanager

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function is called when the FastAPI app starts and stops.
    It creates the database and tables when the app starts.
    """
    create_db_and_tables()
    yield
    # Here you can add any cleanup code if needed when the app stops, e.g: shutdown, closing connections, etc.

app = FastAPI(lifespan=lifespan)

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    """
    Create a new item in the database.
    """
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
    return item

@app.get("/items/", response_model=List[Item])
async def get_items() -> List[Item]:
    """
    Retrieve all items from the database.
    """
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
    return items

def drop_table():
    """
    Drop the Item table from the database. Or this will do the same:
    # This executes a raw SQL command
    with engine.connect() as connection:
        # For PostgreSQL/Supabase:
        connection.execute("DROP TABLE IF EXISTS item CASCADE;")
    """
    SQLModel.metadata.drop_all(engine, tables=[Item.__table__])


# Use the if __name__ == "__main__": block so it only runs when you run the script directly (not when uvicorn imports it):
# if you run uvicorn superbase_learning:app --reload, the drop_table() line won’t run. To drop the table, explicit run `python superbase_learning.py` in your terminal.
if __name__ == "__main__":
    # This will ONLY run if you do: python superbase_learning.py
    drop_table()