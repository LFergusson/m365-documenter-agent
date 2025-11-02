"""Agent client for generating documentation for graph api responses."""

import logging
import os
from azure.identity import DefaultAzureCredential
from shared.helpers.agents.agent_client import BaseAgent

from shared.models.agent_instruction import AgentFewShotInstruction
from shared.tools.graph import GraphTool
import shared.models.configuration as config

# Get logger (logging should be configured by main application)
logger = logging.getLogger(__name__)


class GraphDocumenterAgent(BaseAgent):
    """Agent client for generating documentation for graph schemas."""

    example_1 = (
        """
{
    "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#identity/conditionalAccess/policies/$entity",
    "@microsoft.graph.tips": "Use $select to choose only the properties your app needs, as this can lead to performance improvements. For example: GET identity/conditionalAccess/policies('<guid>')?$select=conditions,createdDateTime",
    "id": "973d7179-c85e-4648-b8cf-32f8a18f0502",
    "templateId": null,
    "displayName": "BLOCK - High Risk Sign-Ins",
    "createdDateTime": "2023-07-16T04:53:13.0783289Z",
    "modifiedDateTime": "2023-08-06T10:36:25.7936777Z",
    "state": "enabledForReportingButNotEnforced",
    "sessionControls": null,
    "conditions": {
        "userRiskLevels": [],
        "signInRiskLevels": [
            "high"
        ],
        "clientAppTypes": [
            "all"
        ],
        "servicePrincipalRiskLevels": [],
        "insiderRiskLevels": null,
        "locations": null,
        "devices": null,
        "clientApplications": null,
        "authenticationFlows": null,
        "applications": {
            "includeApplications": [
                "All"
            ],
            "excludeApplications": [],
            "includeUserActions": [],
            "includeAuthenticationContextClassReferences": [],
            "applicationFilter": null
        },
        "users": {
            "includeUsers": [
                "All"
            ],
            "excludeUsers": [],
            "includeGroups": [],
            "excludeGroups": [
                "a68ee561-2427-4058-b307-7e2f7b8f6c07"
            ],
            "includeRoles": [],
            "excludeRoles": [],
            "includeGuestsOrExternalUsers": null,
            "excludeGuestsOrExternalUsers": null
        },
        "platforms": {
            "includePlatforms": [
                "all"
            ],
            "excludePlatforms": [
                "iOS"
            ]
        }
    },
    "grantControls": {
        "operator": "OR",
        "builtInControls": [
            "block"
        ],
        "customAuthenticationFactors": [],
        "termsOfUse": [],
        "authenticationStrength@odata.context": "https://graph.microsoft.com/v1.0/$metadata#identity/conditionalAccess/policies('973d7179-c85e-4648-b8cf-32f8a18f0502')/grantControls/authenticationStrength/$entity",
        "authenticationStrength": null
    }
}
        """,
        """
    # Conditional Access Policy Configuration

    ## BLOCK - High Risk Sign-Ins - 
    **Policy ID:** 973d7179-c85e-4648-b8cf-32f8a18f0502  
    **State:** Enabled for Reporting But Not Enforced  
    **Created:** July 16, 2023  
    **Last Modified:** August 6, 2023s.

    *This policy blocks all high-risk sign-ins across all applications and platforms except iOS.*

    ### Conditions
    The following values dictate which sign ins match this policy.
    #### User Conditions
    | Configuration Item | Value |
    | ---- | ---- |
    | Include Users | All |
    | Exclude Users | Not Configured |
    | Include Groups | Not Configured |
    | Exclude Groups | a68ee561-2427-4058-b307-7e2f7b8f6c07 |
    | Include Roles | Not Configured |
    | Exclude Roles | Not Configured |
    | Include Guests or External Users | Not Configured |
    | Exclude Guest or External Users | Not Configured |

    #### Risk Based Conditions
    | Configuration Item | Value |
    | ---- | ---- |
    | User Risk Level | Not Configured |
    | Sign In Risk Level | High |
    | Service Principal Risk Levels | Not Configured |
    | Insider Risk Levels | Not Configured |

    #### Location Conditions
    | Configuration Item | Value |
    | ---- | ---- |
    | Locations | Not Configured |

    #### Device and Platform Conditions
    | Configuration Item | Value |
    | ---- | ---- |
    | Devices | Not Configured |
    | Include Platforms | All |
    | Exclude Platforms | iOS |

    #### Authentication Conditions
    | Configuration Item | Value |
    | ---- | ---- |
    | Authentication Flows | Not Configured |
    | Client Applications | Not Configured |
    | Client App Types | All |

    #### Target Application Conditions 
    | Configuration Item | Value |
    | ---- | ---- |
    | Include Applications | All |
    | Exclude Applications | Not Configured |
    | Include User Actions | Not Configured |
    | Include Authentication Context Class References | Not Configured |
    | Application Filters | Not Configured |

    ### Controls
    The following values dictate what controls get applied to a matching sign in.
    #### Grant Controls
    | Configuration Item | Value |
    | ---- | ---- |
    | Operator | Or |
    | Built in Controls | Block |
    | Custom Authentication Factors | Not Configured |
    | Terms of Use | Not Configured |
    | Authentication Strength | Not Configured |
    #### Session Controls
    Not Configured
        """,
    )

    few_shot_example = AgentFewShotInstruction(
        system_instruction="""
You are an expert technical writer specializing in Microsoft Graph API documentation. Your task is to generate clear, concise, and well-structured documentation based on raw JSON responses from the Microsoft Graph API. The documentation should be suitable for inclusion in official Microsoft documentation or technical blogs.
Given a JSON response, extract the relevant configuration details and present them in a human-readable format. Use markdown syntax to create headings, subheadings, and tables where appropriate. Ensure that the documentation accurately reflects the settings and configurations represented in the JSON.
If there are any GUIDs or Ids present in the JSON, use your tools to look up their friendly names and include those in the documentation for better clarity.
        """,
        examples=[example_1],
    )

    config_factory = config.get_configuration_factory()
    active_config = config_factory.create_configuration()

    def __init__(self):
        logger.info("Initializing Graph Documenter Agent.")

        self.graph_tool = GraphTool(
            identity=DefaultAzureCredential(),
            graph_endpoint="https://graph.microsoft.com/",
            paging_enabled=True,
        )

        super().__init__(
            instructions=self.few_shot_example,
            name="GraphDocumenterAgent",
            chat_completion_model=self.active_config.get_standard_chat_model(),
            use_content_safety=False,
        )

    def _setup_agent(self):
        """Set up Graph Documenter Agent specific configuration."""
        logger.info("Setting up Graph Documenter Agent configuration.")
        # Additional setup can be done here if needed.

        self.tools.append(self.graph_tool.get_resource)

    def get_env_var(self, var_name: str) -> str:
        """Retrieve environment variable value."""
        value = os.getenv(var_name)
        if value is None:
            logger.warning(f"Environment variable {var_name} is not set.")
        return value or ""
