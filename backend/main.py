"""
backend/main.py
FastAPI application entry point.
"""

 
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import Config
from backend.api.routes import router

app = FastAPI(
    title="Insurance Support AI",
    description="Multi-agent insurance customer support system",
    version="1.0.0",
)

 
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Insurance Support AI is running. See /docs for API reference."}
