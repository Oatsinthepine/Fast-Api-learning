"""
This backend.py is a practice for setting the backend for a React app using FastAPI. The practice points to the
React-ts/practice/Hello.tsx file, which is a simple React component that fetches data from this FastAPI backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from my React app
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/hello")
async def read_hello():
    return {"message": "Hello from FastAPI!"}