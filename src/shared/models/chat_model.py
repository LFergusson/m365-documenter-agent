from dataclasses import dataclass
import enum


@dataclass
class ChatModelConfig:
    """Configuration for chat models."""

    endpoint: str
    deployment_name: str


# The types of chat models available to power each agent. These will be configured by the configuration class.
class ChatModelType(enum.Enum):
    """Enumeration of chat model types."""

    ADVANCED = "advanced"
    MINI = "mini"
    STANDARD = "standard"
