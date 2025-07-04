from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

# dummy json data for practice
dummy_data = {
  "user_id": 101,
  "name": "Jacky",
  "email": "jacky@example.com",
  "is_active": True,
  "address": {
    "street": "123 FastAPI Lane",
    "city": "Melbourne",
    "postcode": "3000",
    "country": "Australia"
  },
  "orders": [
    {
      "order_id": 5001,
      "item": "Mechanical Keyboard",
      "quantity": 1,
      "price": 120.5
    },
    {
      "order_id": 5002,
      "item": "Wireless Mouse",
      "quantity": 2,
      "price": 45.0
    }
  ],
  "preferences": {
    "newsletter": True,
    "notifications": ["email", "sms"]
  }
}



# To start the server, run this command in the terminal: uvicorn main:app --reload
app = FastAPI()

# This is the home page
@app.get("/")
async def root():
    return {"message": "Hello World"}

# end-point parameter example, it used to allow users to pass data in the url
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/add/{a}/{b}")
async def add(a:int, b:float):
    return {"result": a + b}


# This is a path parameter example. Path parameters are part of the URL path itself.
# The Path() function is used to declare metadata and validation for path parameters.
# Here, it specifies that user_id is required, provides a description, and can be further validated (e.g., gt, lt).
@app.get ("/get_user/{user_id}")
async def get_user(user_id: int = Path(..., description="The id of the user you want to search"), gt=0, lt=200) -> dict:
    if user_id == dummy_data["user_id"]:
        return dummy_data
    else:
        return {"error": "User not found"}


# query parameters example. Query parameters are appended after a ? in the URL, often for filtering, searching, or optional settings.
# Here, we use Optional to indicate that the parameter is not required and the default value is None.
@app.get("/search_item_by_quantity/")
async def search_item_by_quantity(quantity: Optional[int] = None) -> list[dict] | dict:
    result_dict = []
    for order in dummy_data["orders"]:
        if order["quantity"] == quantity:
            result_dict.append({"order": order["item"], "quantity": order["quantity"]})
    return result_dict if result_dict else {"Data":"No items found with the specified quantity"}


# combining path and query parameters together example.
# Here is a structured, practical FastAPI mini-exercise:

#  Combining path + query parameters
#  Using optional and required query parameters
#  Practicing multiple optional filters together

# Mini Project Scenario: Orders API

# You have:
# 	•	A user can retrieve their orders by user_id (path parameter).
# 	They can optionally filter:
# 	•	By item name (optional query param, str)
# 	•	By min_price (optional query param, float)
# 	•	By max_price (optional query param, float)
# 	•	By quantity (optional query param, int)

# ------------------------------
# In-memory dummy data to simulate a database.
# Note: This data is not persistent and will reset when the server restarts.
# ------------------------------
dummy_data_2 = {
    101: [  # user_id = 101
        {"order_id": 5001, "item": "Mechanical Keyboard", "quantity": 1, "price": 120.5},
        {"order_id": 5002, "item": "Wireless Mouse", "quantity": 2, "price": 45.0},
        {"order_id": 5003, "item": "Laptop Stand", "quantity": 1, "price": 30.0},
        {"order_id": 5004, "item": "Wireless Mouse", "quantity": 1, "price": 50.0}
    ],
    102: [  # user_id = 102
        {"order_id": 6001, "item": "USB-C Hub", "quantity": 1, "price": 25.0}
    ]
}

# To use multiple query parameters, this is the correct way doing it: http://127.0.0.1:8000/users/101/?param1=value1&param2=value2&param3=value3
# e.g: http://127.0.0.1:8000/users/101/?min_price=95.0&quantity=1
@app.get("/users/{user_id}/")
async def get_user_orders(
    user_id: int,
    item: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    quantity: Optional[int] = None
):
    user_orders = dummy_data_2.get(user_id, [])
    results = []

    for order in user_orders:
        if item and item.lower() not in order["item"].lower():
            continue
        if min_price is not None and order["price"] < min_price:
            continue
        if max_price is not None and order["price"] > max_price:
            continue
        if quantity is not None and order["quantity"] != quantity:
            continue
        results.append(order)

    return {"user_id": user_id, "filters_applied": {
        "item": item, "min_price": min_price, "max_price": max_price, "quantity": quantity
    }, "results": results}


# Request Body and the POST method example.
# ------------------------------
# Why we use BaseModel:
# ------------------------------
# In FastAPI, we use Pydantic's BaseModel to:
#  Define the expected structure of incoming JSON data (request body).
#  Automatically validate data types (e.g., order_id must be int).
#  Parse incoming data into a Python object we can easily work with.
#  Auto-generate OpenAPI docs (/docs) with clear schema definitions.
# This ensures the client sends the correct data format and prevents type errors during processing.
# ------------------------------

class Order(BaseModel):
    order_id: int
    item: str
    quantity: int
    price: float

# ------------------------------
# POST endpoint to create a new order for a user.
# Path: /create_order/{user_id}
# Method: POST
# - Accepts user_id as a path parameter (int).
# - Accepts an Order JSON payload in the request body, parsed & validated by Pydantic.
# - Adds the order to the user's order list in dummy_data_2.
# - Returns a confirmation message and the order data.
# ------------------------------
@app.post("/create_order/{user_id}")
async def create_order(user_id: int, order: Order) -> dict:
    # Check if the order_id already exists for this user to prevent duplicates
    if any(existing_order["order_id"] == order.order_id for existing_order in dummy_data_2.get(user_id, [])):
        return {"error": "Order ID already exists for this user"}

    # If user_id is not found, create a new user entry and add the order
    if user_id not in dummy_data_2:
        dummy_data_2[user_id] = []
        dummy_data_2[user_id].append(order.model_dump())  # .model_dump() converts Pydantic object to a dict
        return {
            "message": "User not found, created new user and added order",
            "order": order.model_dump()
        }
    else:
        # If user exists, append the new order to their order list
        dummy_data_2[user_id].append(order.model_dump())
        return {
            "message": "Order created successfully",
            "order": order.model_dump()
        }

