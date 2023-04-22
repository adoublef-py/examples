from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .internal.routes import router as internal_router

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

app.include_router(internal_router)
