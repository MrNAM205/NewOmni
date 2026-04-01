import re
from typing import List


def detect_dates(text: str) -> List[str]:
    # Matches formats like: April 12, 2026 | 04/12/2026 | 4/12/26
    pattern = r"\b(?:\d{1,2}/\d{1,2}/\d{2,4}|[A-Za-z]+\s+\d{1,2},\s+\d{4})\b"
    return re.findall(pattern, text)


def detect_amounts(text: str) -> List[str]:
    pattern = r"\$\s?\d+(?:,\d{3})*(?:\.\d{2})?"
    return re.findall(pattern, text)


def detect_reference_numbers(text: str) -> List[str]:
    pattern = r"\b(?:Ref|Reference|Account|Citation|Case)\s*[:#]?\s*\w+\b"
    return re.findall(pattern, text)


def detect_agencies(text: str) -> List[str]:
    pattern = r"\b(?:Department|Office|Agency|Court|Clerk|Bureau)\b.*"
    return re.findall(pattern, text)


def detect_instructions(text: str) -> List[str]:
    pattern = r"\b(?:You must|Please|Required|Submit|Send|Detach|Mail|Pay)\b.*"
    return re.findall(pattern, text)
