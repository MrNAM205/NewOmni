import re
from ..utils import normalize_date, normalize_amount

class PowerCoTemplate:
    issuer_name = "PowerCo"
    detection_keywords = ["powerco", "power co"]

    @staticmethod
    def detect(text: str) -> bool:
        """Detects if the text is from PowerCo."""
        t = text.lower()
        return any(keyword in t for keyword in PowerCoTemplate.detection_keywords)

    @staticmethod
    def extract_fields(text: str) -> dict:
        """Extracts fields from a PowerCo bill with confidence scores."""
        fields: dict[str, dict] = {}

        # PowerCo uses "Customer Number" instead of "Account Number"
        acct = re.search(r"Customer Number:\s*(\d{4}-\d{4}-\d{4})", text, re.IGNORECASE)
        if acct:
            fields["account_number"] = {"value": acct.group(1), "confidence": 0.98}

        # PowerCo's date format is "Month Day, Year"
        stmt_date = re.search(r"Statement Date:\s*([A-Za-z]+ \d{1,2}, \d{4})", text, re.IGNORECASE)
        if stmt_date:
            normalized_date = normalize_date(stmt_date.group(1))
            if normalized_date:
                fields["statement_date"] = {"value": normalized_date, "confidence": 0.98}

        due = re.search(r"Payment Due:\s*([A-Za-z]+ \d{1,2}, \d{4})", text, re.IGNORECASE)
        if due:
            normalized_date = normalize_date(due.group(1))
            if normalized_date:
                fields["due_date"] = {"value": normalized_date, "confidence": 0.98}

        # PowerCo has "Total Amount Due"
        amt = re.search(r"Total Amount Due:\s*\$([0-9,]+\.\d{2})", text, re.IGNORECASE)
        if amt:
            normalized_amount = normalize_amount(amt.group(1))
            if normalized_amount is not None:
                fields["amount_due"] = {"value": normalized_amount, "confidence": 0.98}

        return fields
