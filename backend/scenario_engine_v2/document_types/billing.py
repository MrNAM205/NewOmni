import re
from .base import DocumentAnalyzer
from .utils import normalize_date, normalize_amount
from .issuer_templates.powerco_template import PowerCoTemplate

# In a real system, this would be loaded dynamically
ISSUER_TEMPLATES = [PowerCoTemplate]

class BillingStatementAnalyzer(DocumentAnalyzer):
    """
    Analyzer for generic billing statements (utilities, credit cards, telecom, etc.).
    Detects whether text looks like a billing statement and extracts common fields.
    """

    @staticmethod
    def detect(text: str) -> bool:
        """
        Lightweight detection logic for billing statements.
        """
        t = text.lower()
        keywords = [
            "statement",
            "billing",
            "amount due",
            "total due",
            "due date",
            "previous balance",
            "current charges",
            "account number",
        ]
        return any(k in t for k in keywords)

    @staticmethod
    def extract_fields(text: str) -> dict:
        """
        Extracts and normalizes common billing statement fields, using issuer-specific
        templates if available.
        """
        # Check for a matching issuer template first
        for template in ISSUER_TEMPLATES:
            if template.detect(text):
                # Add issuer name to the fields
                fields = template.extract_fields(text)
                fields["issuer"] = template.issuer_name
                return fields

        # Fall back to generic extraction if no template matches
        return BillingStatementAnalyzer._extract_generic_fields(text)

        @staticmethod
        def _extract_generic_fields(text: str) -> dict:
            """
            Generic field extraction logic with confidence scoring.
            """
            fields: dict[str, dict] = {}
    
            # Account number
            acct = re.search(
                r"(account number|acct\.?\s*#?)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
                text,
                re.IGNORECASE,
            )
            if acct:
                fields["account_number"] = {"value": acct.group(2), "confidence": 0.8}
    
            # Statement date
            stmt_date = re.search(
                r"(statement date)\s*[:\-]?\s*([A-Za-z0-9\/\-\., ]+)",
                text,
                re.IGNORECASE,
            )
            if stmt_date:
                normalized_date = normalize_date(stmt_date.group(2).strip())
                if normalized_date:
                    fields["statement_date"] = {"value": normalized_date, "confidence": 0.95}
                else:
                    fields["statement_date"] = {"value": stmt_date.group(2).strip(), "confidence": 0.8}
    
            # Due date
            due = re.search(
                r"(due date)\s*[:\-]?\s*([A-Za-z0-9\/\-\., ]+)",
                text,
                re.IGNORECASE,
            )
            if due:
                normalized_date = normalize_date(due.group(2).strip())
                if normalized_date:
                    fields["due_date"] = {"value": normalized_date, "confidence": 0.95}
                else:
                    fields["due_date"] = {"value": due.group(2).strip(), "confidence": 0.8}
    
            # Amount due / total due
            amt = re.search(
                r"(amount due|total due)\s*[:\-]?\s*\$?\s*([0-9\.,]+)",
                text,
                re.IGNORECASE,
            )
            if amt:
                normalized_amount = normalize_amount(amt.group(2))
                if normalized_amount is not None:
                    fields["amount_due"] = {"value": normalized_amount, "confidence": 0.95}
                else:
                    fields["amount_due"] = {"value": amt.group(2), "confidence": 0.8}
    
            # Billing period
            period = re.search(
                r"(billing period)\s*[:\-]?\s*([A-Za-z0-9\/\-\., ]+)",
                text,
                re.IGNORECASE,
            )
            if period:
                fields["billing_period"] = {"value": period.group(2).strip(), "confidence": 0.8}
    
            # Optional: previous balance
            prev = re.search(
                r"(previous balance)\s*[:\-]?\s*\$?\s*([0-9\.,]+)",
                text,
                re.IGNORECASE,
            )
            if prev:
                normalized_amount = normalize_amount(prev.group(2))
                if normalized_amount is not None:
                    fields["previous_balance"] = {"value": normalized_amount, "confidence": 0.95}
                else:
                    fields["previous_balance"] = {"value": prev.group(2), "confidence": 0.8}
    
            # Optional: current charges
            curr = re.search(
                r"(current charges)\s*[:\-]?\s*\$?\s*([0-9\.,]+)",
                text,
                re.IGNORECASE,
            )
            if curr:
                normalized_amount = normalize_amount(curr.group(2))
                if normalized_amount is not None:
                    fields["current_charges"] = {"value": normalized_amount, "confidence": 0.95}
                else:
                    fields["current_charges"] = {"value": curr.group(2), "confidence": 0.8}
    
            return fields
    
        @staticmethod
        def administrative_context(fields: dict) -> str:
            """
            Explains the modern administrative meaning of the extracted fields.
            """
            parts: list[str] = []
    
            if "amount_due" in fields:
                parts.append(
                    "The 'amount due' is the total the issuer expects you to pay for this billing cycle."
                )
    
            if "due_date" in fields:
                parts.append(
                    "The 'due date' is when payment must be received to avoid late fees or penalties."
                )
    
            if "account_number" in fields:
                parts.append(
                    "The 'account number' identifies your customer record and is used to match payments and inquiries."
                )
    
            if "billing_period" in fields:
                parts.append(
                    "The 'billing period' defines the range of dates covered by the charges on this statement."
                )
    
            if "previous_balance" in fields or "current_charges" in fields:
                parts.append(
                    "Previous balance and current charges show how the total amount due was calculated."
                )
    
            return " ".join(parts)
    
        @staticmethod
        def historical_context(fields: dict) -> str:
            """
            Provides historical/archival context without giving legal advice.
            """
            parts: list[str] = []
    
            if fields:
                parts.append(
                    "Billing statements evolved from itemized ledgers used in commercial bookkeeping, "
                    "where balances and due dates structured ongoing credit relationships."
                )
    
            if "account_number" in fields:
                parts.append(
                    "Account numbers historically mirrored ledger identifiers used to track individual customer accounts."
                )
    
            if "due_date" in fields:
                parts.append(
                    "Due dates reflect long‑standing commercial practices around credit terms and payment expectations."
                )
    
            return " ".join(parts)
