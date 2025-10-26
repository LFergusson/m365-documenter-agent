"""Agent Client to create a generic Agent."""

from agent_framework.azure import (
    AzureOpenAIChatClient,
)  # pylint: disable=no-name-in-module
from agent_framework import ChatAgent
from azure.identity import DefaultAzureCredential

from shared.models.chat_model import ChatModelConfig
from shared.models.agent_instruction import AgentInstruction


# Create a client to handle creating a generic Agent.
class AgentClient:
    """Abstract base class for agent clients."""

    # The instructions that the agent will respond with.
    instruction: AgentInstruction

    # The name of the agent.
    name: str

    # Whether the agent should send content safety checks.
    use_content_safety: bool = True

    # The Azure Open AI Chat Client.
    agent_client: AzureOpenAIChatClient

    # The agent instance.
    agent: ChatAgent

    def __init__(
        self,
        instruction: AgentInstruction,
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
        self.agent = ChatAgent(
            name=self.name,
            instruction=str(self.instruction),
            chat_client=self.agent_client,
            use_content_safety=self.use_content_safety,
        )

    async def run_agent(self, user_input: str) -> str:
        """Run the agent with the given user input."""
        if not self.agent:
            self.create_agent()

        if self.use_content_safety:
            # TODO: Implement content safety checks here
            pass

        response = await self.agent.run(user_input)
        return response.text
