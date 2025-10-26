# Few Shot Examples
# Input
```Json
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
```
## Output:
```Md
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
```