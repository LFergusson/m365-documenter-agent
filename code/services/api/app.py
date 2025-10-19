"""API Service - FastAPI Application"""
from fastapi import FastAPI
from shared.models import TestStatusResponse

app = FastAPI(
    title="Browser Agent API",
    description="API service for browser automation and analysis",
    version="0.1.0"
)


@app.get("/status", response_model=TestStatusResponse)
async def get_status():
    """Endpoint to get the status of the application."""
    return TestStatusResponse()


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    return {"status": "healthy", "service": "api"}
