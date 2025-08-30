import sys
sys.dont_write_bytecode = True

import json
import pathlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware


from src.models.api import *

from src.services.database import create_new_db_conn

from src.config.logger_config import logger
from src.config.settings import settings
logger.info("Starting FastAPI app")


app = FastAPI(
    title = "GenAI Dashboard Backend",
    description = "Backend service for GenAI Dashboard",
    root_path="/genai-backend",
    version = "0.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/v0/health', summary="Health check", description="Returns service health status.")
async def health_check():
    return {"status": "ok"}

@app.post("/api/v0/new-database-connection", response_model=CreateDBConnResponse, summary="Create a new database connection", description="Creates a new database connection with the provided details.")
async def create_database_connection(request: DatabaseConnectionRequest):
    try:
        result = create_new_db_conn(request)
        return result
    except Exception as e:
        logger.error(f"Error in /new-database-connection: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/v0/new-session", response_model=SessionResponse, summary="Generate a new session for the user", description="Creates a new session for the user with the provided context data. This is created for each chat window you open. The session ID is used to track the conversation and context for the user.")
async def generate_new_session(request_data: UserSessionRequest):
    pass
