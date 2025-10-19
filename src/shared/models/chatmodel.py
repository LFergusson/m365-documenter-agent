from dataclasses import dataclass


@dataclass
class ChatModelConfig:
    """Configuration for chat models."""

    endpoint: str
    deployment_name: str
