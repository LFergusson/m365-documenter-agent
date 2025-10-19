"""API Service - FastAPI Application"""

import logging
from fastapi import FastAPI
from shared.models.chatmodel import ChatModelConfig
from shared.models.responses import TestStatusResponse
from shared.helpers.agents import agent_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Browser Agent API",
    description="API service for browser automation and analysis",
    version="0.1.0",
)

chat_config = ChatModelConfig(
    endpoint="https://aoai-browseragent6cpbv-dev.openai.azure.com/",
    deployment_name="gpt-4o",
)


@app.get("/status", response_model=TestStatusResponse)
async def get_status():
    """Endpoint to get the status of the application."""
    return TestStatusResponse()


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    return {"status": "healthy", "service": "api"}


@app.post("/run-agent")
async def run_agent(user_input: str):
    """Endpoint to run the agent with user input."""
    logger.warning("Received request to run agent.")
    # Check that the body user_input is provided.
    if not user_input:
        return {"error": "user_input is required."}

    # Initialize the agent client (example parameters used here).
    agent = agent_client.AgentClientBase(
        instruction="You are a helpful assistant.",
        name="TestAgent",
        chat_completion_model=chat_config,
    )

    agent.create_agent()

    response = await agent.run_agent(user_input)
    return {"response": response}
