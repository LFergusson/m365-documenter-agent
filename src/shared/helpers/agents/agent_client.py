"""Agent Client to create a generic Agent."""

from agent_framework.azure import (
    AzureOpenAIChatClient,
)  # pylint: disable=no-name-in-module
from agent_framework import ChatAgent
from azure.identity import DefaultAzureCredential
from abc import ABC

from shared.models.chat_model import ChatModelConfig
from shared.models.agent_instruction import AgentInstruction


# Create a client to handle creating a generic Agent.
class BaseAgent(ABC):
    """Abstract base class for agent clients."""

    def __init__(
        self,
        instructions: AgentInstruction,
        name: str,
        chat_completion_model: ChatModelConfig,
        use_content_safety: bool = True,
    ):
        # Initialize the agent client variables.
        self.instructions = instructions
        self.name = name
        self.use_content_safety = use_content_safety
        self.chat_completion_model = chat_completion_model

        self.agent_client = AzureOpenAIChatClient(
            endpoint=chat_completion_model.endpoint,
            deployment_name=chat_completion_model.deployment_name,
            credential=DefaultAzureCredential(),
        )

        self._create_agent()

    def __repr__(self):
        return f"BaseAgent(name={self.name}, instructions={self.instructions})"

    # Function To create the Agent
    def _setup_agent(self):
        """Set up Agent Specific configuration."""
        pass

    def _create_agent(self):
        """Create the agent instance."""
        self._setup_agent()
        self.agent = ChatAgent(
            chat_client=self.agent_client,
            instructions=str(self.instructions),
            name=self.name,
        )

    async def run(self, user_input: str) -> str:
        """Run the agent with user input and return the response."""
        response = await self.agent.run(user_input)
        return response.text
