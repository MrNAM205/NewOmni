import re
from typing import Protocol

class IssuerTemplate(Protocol):
    """
    Protocol for issuer-specific billing statement parsers.
    """
    issuer_name: str
    detection_keywords: list[str]

    @staticmethod
    def detect(text: str) -> bool:
        """Detects if the text belongs to this issuer."""
        ...

    @staticmethod
    def extract_fields(text: str) -> dict:
        """Extracts fields using issuer-specific logic."""
        ...
