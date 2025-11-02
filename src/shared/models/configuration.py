"""
Improved configuration management with proper singleton pattern and factory design.
"""

from abc import ABC, abstractmethod
from enum import Enum
import os
import json
import logging
import threading
from dataclasses import dataclass
from typing import Optional, Type
from agent_framework.azure import AzureOpenAIChatClient

logger = logging.getLogger(__name__)


class ModelTypes(Enum):
    """Enumeration of model types."""

    CHAT = "chat"
    EMBEDDING = "embedding"


@dataclass
class ModelConfiguration:
    """AI Model configuration settings."""

    name: str
    type: ModelTypes
    deployment_name: str
    endpoint: str

    @classmethod
    def from_dict(cls, model_dict: dict) -> "ModelConfiguration":
        """Create a ModelConfiguration instance from a dictionary."""
        return cls(
            name=model_dict["name"],
            type=ModelTypes[model_dict["type"].upper()],
            deployment_name=model_dict["deployment_name"],
            endpoint=model_dict["endpoint"],
        )

    def to_dict(self) -> dict:
        """Convert the ModelConfiguration instance to a dictionary."""
        return {
            "name": self.name,
            "type": self.type.value,
            "deployment_name": self.deployment_name,
            "endpoint": self.endpoint,
        }

    def to_azure_oai_chat_client(self, credential) -> AzureOpenAIChatClient:
        """Create an AzureOpenAIChatClient instance from the model configuration."""
        if self.type != ModelTypes.CHAT:
            raise ValueError(
                "ModelConfiguration type must be CHAT to create a chat client."
            )
        return AzureOpenAIChatClient(
            endpoint=self.endpoint,
            deployment_name=self.deployment_name,
            credential=credential,
        )


class Configuration(ABC):
    """
    Abstract base class for application configuration.
    Defines the interface for configuration implementations.
    """

    def __init__(self):
        self._standard_chat_model: Optional[ModelConfiguration] = None
        self._simple_chat_model: Optional[ModelConfiguration] = None
        self._text_embedding_model: Optional[ModelConfiguration] = None

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the configuration. Must be implemented by subclasses."""
        pass

    # Getter methods
    def get_standard_chat_model(self) -> ModelConfiguration:
        """Get the standard chat model configuration."""
        if self._standard_chat_model is None:
            raise RuntimeError("Configuration not initialized")
        return self._standard_chat_model

    def get_simple_chat_model(self) -> ModelConfiguration:
        """Get the simple chat model configuration."""
        if self._simple_chat_model is None:
            raise RuntimeError("Configuration not initialized")
        return self._simple_chat_model

    def get_text_embedding_model(self) -> ModelConfiguration:
        """Get the text embedding model configuration."""
        if self._text_embedding_model is None:
            raise RuntimeError("Configuration not initialized")
        return self._text_embedding_model

    # Setter methods (protected)
    def _set_standard_chat_model(self, model_config: ModelConfiguration) -> None:
        """Set the standard chat model configuration."""
        self._standard_chat_model = model_config

    def _set_simple_chat_model(self, model_config: ModelConfiguration) -> None:
        """Set the simple chat model configuration."""
        self._simple_chat_model = model_config

    def _set_text_embedding_model(self, model_config: ModelConfiguration) -> None:
        """Set the text embedding model configuration."""
        self._text_embedding_model = model_config


class LocalConfiguration(Configuration):
    """Local file-based configuration implementation."""

    def __init__(self, config_path: Optional[str] = None):
        super().__init__()
        self._config_path = config_path or self._get_default_config_path()

    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        env_path = os.getenv("LOCAL_CONFIG_PATH")
        if env_path:
            return env_path
        return os.path.join(os.path.dirname(__file__), "default_config.json")

    def initialize(self) -> None:
        """Initialize configuration from local file."""
        logger.info("Loading configuration from: %s", self._config_path)

        if not os.path.exists(self._config_path):
            raise FileNotFoundError(
                f"Configuration file not found: {self._config_path}"
            )

        try:
            with open(self._config_path, "r", encoding="utf-8") as file:
                config_data = json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            raise RuntimeError(f"Failed to load configuration: {e}") from e

        try:
            deployments = config_data["model_deployments"]
            self._set_standard_chat_model(
                ModelConfiguration.from_dict(deployments["standard_chat_model"])
            )
            self._set_simple_chat_model(
                ModelConfiguration.from_dict(deployments["simple_chat_model"])
            )
            self._set_text_embedding_model(
                ModelConfiguration.from_dict(deployments["text_embedding_model"])
            )
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"Invalid configuration format: {e}") from e

        logger.info("Configuration loaded successfully")


class OnlineConfiguration(Configuration):
    """Online/remote configuration implementation."""

    def __init__(self, endpoint: str, api_key: str):
        super().__init__()
        self.endpoint = endpoint
        self.api_key = api_key

    def initialize(self) -> None:
        """Initialize configuration from online source."""
        # Implementation would fetch from remote service
        logger.info("Loading configuration from online source: %s", self.endpoint)
        # Placeholder implementation
        raise NotImplementedError("Online configuration not yet implemented")


class ConfigurationSingleton:
    """
    Thread-safe singleton wrapper for configuration instances.
    Separates singleton concerns from configuration logic.
    """

    _instances: dict[Type[Configuration], Configuration] = {}
    _lock = threading.Lock()

    @classmethod
    def get_instance(
        cls, config_class: Type[Configuration], *args, **kwargs
    ) -> Configuration:
        """Get or create a singleton instance of the specified configuration class."""
        if config_class not in cls._instances:
            logger.info("No existing instance of %s found.", config_class.__name__)
            with cls._lock:
                # Double-check locking pattern
                if config_class not in cls._instances:
                    logger.info("Creating new instance of %s", config_class.__name__)
                    instance = config_class(*args, **kwargs)
                    instance.initialize()
                    cls._instances[config_class] = instance
                else:
                    logger.info(
                        "Returning existing instance of %s", config_class.__name__
                    )
        else:
            logger.info("Returning existing instance of %s", config_class.__name__)
        return cls._instances[config_class]

    @classmethod
    def clear_instances(cls) -> None:
        """Clear all singleton instances. Useful for testing."""
        with cls._lock:
            cls._instances.clear()


class ConfigurationFactory:
    """Factory for creating configuration instances."""

    @staticmethod
    def create_local_configuration(config_path: Optional[str] = None) -> Configuration:
        """Create a local configuration instance."""
        return ConfigurationSingleton.get_instance(LocalConfiguration, config_path)

    @staticmethod
    def create_online_configuration(endpoint: str, api_key: str) -> Configuration:
        """Create an online configuration instance."""
        return ConfigurationSingleton.get_instance(
            OnlineConfiguration, endpoint, api_key
        )

    @staticmethod
    def create_configuration() -> Configuration:
        """Create configuration based on environment detection."""
        # Check if online configuration is available
        online_endpoint = os.getenv("CONFIG_ENDPOINT")
        online_api_key = os.getenv("CONFIG_API_KEY")

        if online_endpoint and online_api_key:
            try:
                return ConfigurationFactory.create_online_configuration(
                    online_endpoint, online_api_key
                )
            except Exception as e:
                logger.warning("Failed to create online configuration: %s", e)
                logger.info("Falling back to local configuration")

        return ConfigurationFactory.create_local_configuration()


# Convenience function for backward compatibility
def get_configuration_factory() -> ConfigurationFactory:
    """Get the configuration factory instance."""
    return ConfigurationFactory()
