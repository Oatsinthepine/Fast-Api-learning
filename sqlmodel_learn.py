# sqlmodel is a modern ORM library for Python, built on top of SQLAlchemy and Pydantic.
from sqlmodel import SQLModel, Field, select
from typing import Optional, List, Any, Coroutine, Sequence
# asynccontextmanager is used to create an async context manager runs when the fastapi app starts
from contextlib import asynccontextmanager
from fastapi import FastAPI

# first, we define the database model class
class Item(SQLModel, table=True):
    """

    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offered: bool = False

from sqlmodel import create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# create the database engine
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    """
    Create the database and tables if they do not exist.
    """
    SQLModel.metadata.create_all(engine)



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function is called when the FastAPI app starts and stops.
    It creates the database and tables when the app starts.
    •	asynccontextmanager lets you use yield to define what happens when the app starts (before yield) and what happens when the app stops (after yield).
	•	When FastAPI starts the app, it runs the code before yield (in this case, setting up DB/tables).
	•	The app stays “running” while “paused” at yield.
	•	When the app is shutting down, FastAPI continues after yield (where you can put cleanup code: closing DB connections, cleaning temp files, etc.).

	1.	App starts:
	•	Runs everything before yield (setup).
	2.	App is running:
	•	Paused at yield (serving requests, etc.).
	3.	App stops:
	•	Runs code after yield (cleanup).
    """
    create_db_and_tables()
    yield
    # Here you can add any cleanup code if needed when the app stops, e.g: shutdown, closing connections, etc.

app = FastAPI(lifespan=lifespan)


from fastapi import Depends
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    """
    This path operation function creates a new item in the database.
    :param item: The item to be created, should be an instance of the Item model.
    :return: the created item.
    """
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

@app.get("/items/", response_model=List[Item])
async def get_items() -> Sequence[Item]:
    """
    This path operation function retrieves all items from the database.
    :return:
    """
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items
