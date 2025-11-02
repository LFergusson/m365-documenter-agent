"""
This module defines configuration models and settings for the application.
It includes model configurations and a singleton configuration class.
"""

from enum import Enum
import os
import json
import logging
from dataclasses import dataclass
from agent_framework.azure import AzureOpenAIChatClient

# Get logger (logging should be configured by main application)
logger = logging.getLogger(__name__)


def get_configuration_factory() -> "ConfigurationFactory":
    """Get the appropriate configuration factory based on environment."""
    online_available = False  # Placeholder for actual online check logic

    if online_available:
        return OnlineConfigurationFactory()
    else:
        return LocalConfigurationFactory()


class ModelTypes(Enum):
    """Enumeration of model types."""

    CHAT = "chat"
    EMBEDDING = "embedding"


@dataclass
class ModelConfiguration:
    """Model configuration settings."""

    name: str
    type: ModelTypes
    deployment_name: str
    endpoint: str

    @classmethod
    def from_dict(cls, model_dict: dict):
        """Create a ModelConfiguration instance from a dictionary.
        Usage ModelConfiguration.from_dict(model_dict)"""
        instance = cls(
            name=model_dict["name"],
            type=ModelTypes[model_dict["type"].upper()],
            deployment_name=model_dict["deployment_name"],
            endpoint=model_dict["endpoint"],
        )
        return instance

    def to_dict(self) -> dict:
        """Convert the ModelConfiguration instance to a dictionary.
        Usage dict = model_config.to_dict()"""
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


class Configuration:
    """
    Application configuration settings.
    Please note this class should never have its __init__ or __new__ methods overridden directly.
    """

    # Singleton Instance Management
    _instance = None
    _initialized = False

    # Chat Models
    _standard_chat_model: ModelConfiguration
    _simple_chat_model: ModelConfiguration

    # Embedding Models
    _text_embedding_model: ModelConfiguration

    # Implementation of Singleton Pattern for Config efficiency.
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Check if already initialized if it is do not reinitialize
        if self._initialized:
            pass
        logger.info("Configuration is not initialized. Initializing now")
        self.initialize_configuration()
        self._initialized = True

    def initialize_configuration(self):
        """
        Initialize configuration settings with the current state
        of the application in the configuration provider.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_standard_chat_model(self) -> ModelConfiguration:
        """Get the standard chat model configuration."""
        return self._standard_chat_model

    def get_simple_chat_model(self) -> ModelConfiguration:
        """Get the simple chat model configuration."""
        return self._simple_chat_model

    def get_text_embedding_model(self) -> ModelConfiguration:
        """Get the text embedding model configuration."""
        return self._text_embedding_model

    def set_standard_chat_model(self, model_config: ModelConfiguration):
        """Set the standard chat model configuration."""
        self._standard_chat_model = model_config

    def set_simple_chat_model(self, model_config: ModelConfiguration):
        """Set the simple chat model configuration."""
        self._simple_chat_model = model_config

    def set_text_embedding_model(self, model_config: ModelConfiguration):
        """Set the text embedding model configuration."""
        self._text_embedding_model = model_config


class ConfigurationFactory:
    """Factory class to create configuration instances."""

    @staticmethod
    def create_configuration() -> Configuration:
        """Create a configuration instance."""
        raise NotImplementedError("This method should be overridden by subclasses.")


class LocalConfigurationFactory(ConfigurationFactory):
    """Factory class to create local configuration instances."""

    @staticmethod
    def create_configuration() -> Configuration:
        """Create a local configuration instance."""
        return LocalConfiguration()


class LocalConfiguration(Configuration):
    """Local configuration settings."""

    # Get the Config File Location from Environment Variable or use default
    _config_file_env_var = "LOCAL_CONFIG_PATH"
    _default_config_path = os.path.join(
        os.path.dirname(__file__), "default_config.json"
    )
    _local_configuration_path: str = ""

    def initialize_configuration(self):
        """Initialize local configuration settings."""
        logger.info(
            "Initializing local configuration from %s", self._local_configuration_path
        )
        self._local_configuration_path = os.getenv(
            self._config_file_env_var, self._default_config_path
        )
        if not os.path.exists(self._local_configuration_path):
            raise FileNotFoundError(
                f"Local configuration file not found at {self._local_configuration_path}"
            )

        with open(self._local_configuration_path, "r", encoding="utf-8") as config_file:
            config_data = config_file.read()

        config_json = json.loads(config_data)

        # Initialize model configurations
        self._standard_chat_model = ModelConfiguration.from_dict(
            config_json["model_deployments"]["standard_chat_model"]
        )
        self._simple_chat_model = ModelConfiguration.from_dict(
            config_json["model_deployments"]["simple_chat_model"]
        )
        self._text_embedding_model = ModelConfiguration.from_dict(
            config_json["model_deployments"]["text_embedding_model"]
        )


class OnlineConfigurationFactory(ConfigurationFactory):
    """Factory class to create online configuration instances."""

    @staticmethod
    def create_configuration() -> Configuration:
        """Create an online configuration instance."""
        return Configuration()
