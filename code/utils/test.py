from dataclasses import dataclass

# Test Status Response
@dataclass
class TestStatusResponse:
    status: str = "ok"