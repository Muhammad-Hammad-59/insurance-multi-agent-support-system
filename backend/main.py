"""
backend/main.py
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.config import Config

load_dotenv()

from backend.api.routes import router

app = FastAPI(
    title="Insurance Support AI",
    description="Multi-agent insurance customer support system",
    version="1.0.0",
)

# Allow local frontend dev server
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=Config.CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://127.0.0.1",
        "http://127.0.0.1:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Insurance Support AI is running. See /docs for API reference."}
