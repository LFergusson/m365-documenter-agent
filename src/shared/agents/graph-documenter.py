from shared.helpers.agents.agent_client import AgentClient
from shared.models.chatmodel import ChatModelType
from shared.models.configuration import AppConfig


class GraphDocumenterAgent:
    """Agent client for generating documentation for graph databases."""

    agent_client: AgentClient
    instructions: str = "Generate documentation for the provided graph database schema."

    def __init__(self, config: AppConfig):
        self.agent_client = AgentClient(
            instruction=self.instructions,
            name="GraphDocumenterAgent",
            chat_completion_model=config.get_chat_model_config(ChatModelType.STANDARD),
            use_content_safety=config.use_content_safety,
        )
