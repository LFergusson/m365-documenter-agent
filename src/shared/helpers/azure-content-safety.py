class ContentSafetyResult:
    """Result of content safety check."""

    is_safe: bool
    issues: list[str]

    def __init__(self, is_safe: bool, issues: list[str]):
        self.is_safe = is_safe
        self.issues = issues


class AzureContentSafetyClient:
    """Client to handle Azure Content Safety checks."""

    def __init__(self, endpoint: str, deployment_name: str, credential):
        self.content_safety_client = AzureContentSafetyClient(
            endpoint=endpoint,
            deployment_name=deployment_name,
            credential=credential,
        )

    async def check_content(self, content: str) -> ContentSafetyResult:
        """Check the content for safety."""
        response = await self.content_safety_client.analyze_text(content)
        return ContentSafetyResult(
            is_safe=response.is_safe,
            issues=response.issues,
        )
