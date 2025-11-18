"""
FeelInk Backend - Main Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import auth_router, users_router, metrics_router, entries_router, analytics_router
from app.utils.database import init_db

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: Cleanup if needed
    pass
from app.api import auth_router, users_router, metrics_router, entries_router, analytics_router, demo_data_router

# Create FastAPI application
app = FastAPI(
    title="FeelInk API",
    description="Backend API for FeelInk - Mental Health & Wellness Tracking PWA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(entries_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(demo_data_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "FeelInk Backend",
        "version": "1.0.0"
    }


# Hello World endpoint (STAGE 0 deliverable)
@app.get("/")
async def root():
    """Root endpoint - Hello World"""
    return {
        "message": "Welcome to FeelInk API! 🎯",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "stage": "STAGE 1 - Backend Foundation Complete ✅"
    }


# API v1 prefix group
@app.get("/api/v1")
async def api_root():
    """API v1 root endpoint"""
    return {
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "metrics": "/api/v1/metrics",
            "entries": "/api/v1/entries"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
