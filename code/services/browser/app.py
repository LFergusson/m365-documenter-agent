"""Example Browser Service - Demonstrates code reuse"""
from fastapi import FastAPI
from shared.models import TestStatusResponse

app = FastAPI(
    title="Browser Service",
    description="Browser automation service",
    version="0.1.0"
)


@app.get("/status", response_model=TestStatusResponse)
async def get_status():
    """Reusing shared status response model"""
    return TestStatusResponse()


@app.get("/browser/info")
async def browser_info():
    """Example browser-specific endpoint"""
    return {
        "service": "browser",
        "capabilities": ["web_scraping", "automation", "screenshots"],
        "status": "ready"
    }

