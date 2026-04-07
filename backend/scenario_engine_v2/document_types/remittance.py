from .utils import normalize_amount
import re
# barcode / OCR-line support will be optional
try:
    from pyzbar.pyzbar import decode as decode_barcode
    from PIL import Image
except ImportError:
    decode_barcode = None
    Image = None

from .base import DocumentAnalyzer

class RemittanceAnalyzer(DocumentAnalyzer):

    @staticmethod
    def detect(text: str) -> bool:
        t = text.lower()
        keywords = [
            "remittance", "payment coupon", "detach and return",
            "payment slip", "remit to", "please return this portion"
        ]
        return any(k in t for k in keywords)

    @staticmethod
    def extract_fields(text: str) -> dict:
        fields: dict[str, dict] = {}

        # Coupon / payment slip ID
        coupon = re.search(r"(coupon|slip|stub)\s*#?\s*[:\-]?\s*([A-Za-z0-9\-]+)", text, re.I)
        if coupon:
            fields["coupon_id"] = {"value": coupon.group(2), "confidence": 0.8}

        # Remit-to address
        remit = re.search(r"(remit to|payment address)\s*[:\-]?\s*(.+)", text, re.I)
        if remit:
            fields["remit_to"] = {"value": remit.group(2).strip(), "confidence": 0.8}

        # Amount enclosed line
        amt = re.search(r"(amount enclosed)\s*[:\-]?\s*\$?([0-9\.,]+)?", text, re.I)
        if amt:
            normalized_amount = normalize_amount(amt.group(2) or "")
            if normalized_amount is not None:
                fields["amount_enclosed"] = {"value": normalized_amount, "confidence": 0.95}
            else:
                fields["amount_enclosed"] = {"value": amt.group(2) or "", "confidence": 0.8}

        # Account reference
        acct = re.search(r"(account number|acct\.?\s*#?)\s*[:\-]?\s*([A-Za-z0-9\-]+)", text, re.I)
        if acct:
            fields["account_number"] = {"value": acct.group(2), "confidence": 0.8}

        return fields

    @staticmethod
    def extract_barcode_data(image_path: str) -> dict:
        """
        Optional: extract barcode data from a remittance coupon image.
        Returns {} if barcode support is unavailable.
        """
        if decode_barcode is None or Image is None:
            return {}

        img = Image.open(image_path)
        codes = decode_barcode(img)

        if not codes:
            return {}

        # For now, just return the first decoded symbol
        code = codes[0]
        return {
            "barcode_type": code.type,
            "barcode_data": code.data.decode("utf-8", errors="ignore"),
        }

    @staticmethod
    def extract_ocr_line(text: str) -> dict:
        """
        Extracts and normalizes a MICR/OCR-style line if present.
        """
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if not lines:
            return {}

        last = lines[-1]
        if re.search(r"[0-9]{6,}", last):
            # Normalize by splitting into components
            parts = re.split(r'\s{2,}', last)
            return {
                "ocr_line": {"value": last, "confidence": 0.85},
                "ocr_line_parts": {"value": parts, "confidence": 0.85}
            }

        return {}

    @staticmethod
    def administrative_context(fields: dict) -> str:
        parts = []

        parts.append(
            "This remittance section is designed to be detached and returned with your payment "
            "so the issuer can automatically match the payment to your account."
        )

        if "coupon_id" in fields:
            parts.append("The coupon or stub ID helps the issuer track this specific payment slip.")

        if "amount_enclosed" in fields:
            parts.append("The 'amount enclosed' field is where you indicate how much you are paying.")

        if "remit_to" in fields:
            parts.append("The 'remit to' address is where physical payments are expected to be sent.")

        return " ".join(parts)

    @staticmethod
    def historical_context(fields: dict) -> str:
        parts = []

        parts.append(
            "Historically, remittance coupons evolved from detachable payment orders used in "
            "mail‑based billing systems."
        )

        if "coupon_id" in fields:
            parts.append(
                "Coupon identifiers mirror earlier practices of using numbered payment slips "
                "to reconcile ledger entries."
            )

        return " ".join(parts)
