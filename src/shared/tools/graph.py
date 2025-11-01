import logging
from typing import Annotated
from pydantic import Field
from agent_framework import ai_function
from agent_framework.observability import get_tracer, get_meter
from azure.identity import DefaultAzureCredential
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphTool:
    """A group of tools used to interact with the Microsoft Graph API."""

    def __init__(
        self,
        identity: DefaultAzureCredential,
        graph_endpoint="https://graph.microsoft.com/v1.0",
        paging_enabled=True,
        version: str = "v1.0",
    ):
        self.identity = identity
        self.graph_endpoint = graph_endpoint
        self.token = identity.get_token(f"{self.graph_endpoint}/.default").token
        self.paging_enabled = paging_enabled
        self.version = version

    def get_resource(
        self,
        path: Annotated[
            str,
            Field(
                description="The resource path to retrieve from Microsoft Graph API. For example, to get user details, use 'users/{user-id}'. To get group details, use 'groups/{group-id}'.",
            ),
        ],
    ) -> str:
        """ "This function takes a resource path and returns the corresponding resource from Microsoft Graph API. This can be used to retrieve information about Microsoft 365 and Entra Resources."""

        request_headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            f"{self.graph_endpoint}/{self.version}/{path}",
            headers=request_headers,
            timeout=30,
        )

        # If the response is not successful, log the error and return an error message to the agent.
        if response.status_code != 200:
            logger.error(
                "Failed to retrieve resource from Graph API. Status code: %s, Response: %s",
                response.status_code,
                response.text,
            )
            tool_output = f"get_resource's graph api request failed with status code {response.status_code} and message: {response.text}"
        else:
            logger.info("Successfully retrieved resource from Graph API.")
            tool_output = response.text

        return tool_output
