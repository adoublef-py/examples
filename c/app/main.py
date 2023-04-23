from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .internal.todos.routes import router as todos_router

origins = [
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(todos_router, prefix="/todos")
