from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
async def get_status():
    '''Endpoint to get the status of the application.'''
    return {"status": "ok"}

