"""Shared response models"""
from dataclasses import dataclass


@dataclass
class TestStatusResponse:
    """Standard status response model"""
    status: str = "ok"
