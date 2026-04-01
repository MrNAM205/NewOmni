from __future__ import annotations

from typing import Dict, Any
from .detectors import (
    detect_dates,
    detect_amounts,
    detect_reference_numbers,
    detect_agencies,
    detect_instructions
)


def extract_fields(text: str) -> Dict[str, Any]:
    return {
        "dates": detect_dates(text),
        "amounts": detect_amounts(text),
        "reference_numbers": detect_reference_numbers(text),
        "agencies": detect_agencies(text),
        "instructions": detect_instructions(text)
    }
