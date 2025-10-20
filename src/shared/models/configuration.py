"""Configuration for the applications."""

from dataclasses import dataclass
from src.shared.models.chatmodel import ChatModelType, ChatModelConfig


@dataclass
class AppConfig:
    """Application configuration settings."""

    chat_model_type: ChatModelType
    chat_model_config: ChatModelConfig

    advanced_model_config: ChatModelConfig = ChatModelConfig(
        endpoint="https://advanced-openai-endpoint/",
        deployment_name="advanced-deployment",
    )

    mini_model_config: ChatModelConfig = ChatModelConfig(
        endpoint="https://mini-openai-endpoint/",
        deployment_name="mini-deployment",
    )

    standard_model_config: ChatModelConfig = ChatModelConfig(
        endpoint="https://standard-openai-endpoint/",
        deployment_name="standard-deployment",
    )

    use_content_safety: bool = False

    def get_chat_model_config(self, model_type: ChatModelType) -> ChatModelConfig:
        if model_type == ChatModelType.ADVANCED:
            return self.advanced_model_config
        elif model_type == ChatModelType.MINI:
            return self.mini_model_config
        elif model_type == ChatModelType.STANDARD:
            return self.standard_model_config
        else:
            raise ValueError(f"Unknown model type: {model_type}")
