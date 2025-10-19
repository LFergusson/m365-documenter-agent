import asyncio
from abc import ABC
from dataclasses import dataclass

from agent_framework.azure import (
    AzureOpenAIChatClient,
)  # pylint: disable=no-name-in-module
from agent_framework import ChatAgent
from azure.identity import DefaultAzureCredential

from shared.models.chatmodel import ChatModelConfig


# Create a client to handle creating a generic Agent.
class AgentClientBase(ABC):
    """Abstract base class for agent clients."""

    instruction: str
    name: str
    use_content_safety: bool = True
    agent_client: AzureOpenAIChatClient
    agent: ChatAgent

    def __init__(
        self,
        instruction: str,
        name: str,
        chat_completion_model: ChatModelConfig,
        use_content_safety: bool = True,
    ):
        self.instruction = instruction
        self.name = name
        self.use_content_safety = use_content_safety
        self.chat_completion_model = chat_completion_model
        self.agent_client = AzureOpenAIChatClient(
            endpoint=chat_completion_model.endpoint,
            deployment_name=chat_completion_model.deployment_name,
            credential=DefaultAzureCredential(),
        )

    # Function To create the Agent
    def create_agent(self):
        """Create the agent client."""
        credential = DefaultAzureCredential()
        self.agent = ChatAgent(
            name=self.name,
            instruction=self.instruction,
            chat_client=self.agent_client,
            use_content_safety=self.use_content_safety,
        )

    async def run_agent(self, user_input: str) -> str:
        """Run the agent with the given user input."""
        if not self.agent:
            self.create_agent()

        response = await self.agent.run(user_input)
        return response.text
