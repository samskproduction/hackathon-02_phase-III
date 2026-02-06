from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import traceback
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from database.database import engine
from models.task import Task
from models.user import User
from routes import tasks, auth
from api import chat
from core.config import settings
from core.logging_config import logger
from core.middleware import ErrorHandlingMiddleware

load_dotenv()

# Create/update tables on startup
def create_db_and_tables():
    logger.info("Creating/updating database tables...")
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Database tables created/updated successfully.")


app = FastAPI(
    title="Task Management API",
    description="Backend API for task management application with JWT authentication",
    version="1.0.0"
)

# Add error handling middleware first
app.add_middleware(ErrorHandlingMiddleware)

# CORS middleware - configure based on your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header for JWT
    expose_headers=["Access-Control-Allow-Origin"]
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    logger.error(traceback.format_exc())

    # Return standardized error response
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "GENERAL_001",
                "message": "Internal server error occurred"
            }
        }
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "GENERAL_002",
                "message": "Database connection error"
            }
        }
    )

# Include routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router)  # Chat router is already prefixed with /api

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Task Management API is running"}

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "backend"}
