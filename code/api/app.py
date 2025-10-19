from fastapi import FastAPI
from ..utils.test import TestStatusResponse
app = FastAPI()

@app.get("/status")
async def get_status():
    '''Endpoint to get the status of the application.'''
    return TestStatusResponse()

