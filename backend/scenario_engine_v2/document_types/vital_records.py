import re
from .base import DocumentAnalyzer
from .utils import normalize_date


class VitalRecordAnalyzer(DocumentAnalyzer):
    """
    Analyzer for vital records, especially birth certificates.
    Focuses on:
      - identifying as a vital record
      - extracting key fields
      - explaining administrative vs historical context
    """

    @staticmethod
    def detect(text: str) -> bool:
        t = text.lower()
        keywords = [
            "birth certificate",
            "certificate of live birth",
            "certificate of birth",
            "vital record",
            "department of health",
            "bureau of vital statistics",
            "state registrar",
            "county registrar",
        ]
        return any(k in t for k in keywords)

    @staticmethod
    def extract_fields(text: str) -> dict:
        fields: dict[str, dict] = {}

        # Child's name
        child = re.search(
            r"(child(?:'s)? name|name of child)\s*[:\-]?\s*([A-Z ,.'\-]+)",
            text,
            re.IGNORECASE,
        )
        if child:
            fields["child_name"] = {"value": child.group(2).strip(), "confidence": 0.8}

        # Date of birth
        dob = re.search(
            r"(date of birth|dob)\s*[:\-]?\s*([A-Za-z0-9\/\-\., ]+)",
            text,
            re.IGNORECASE,
        )
        if dob:
            normalized_date = normalize_date(dob.group(2).strip())
            if normalized_date:
                fields["date_of_birth"] = {"value": normalized_date, "confidence": 0.95}
            else:
                fields["date_of_birth"] = {"value": dob.group(2).strip(), "confidence": 0.8}

        # Place of birth
        pob = re.search(
            r"(place of birth|city and state of birth)\s*[:\-]?\s*([A-Za-z0-9 ,.\-]+)",
            text,
            re.IGNORECASE,
        )
        if pob:
            fields["place_of_birth"] = {"value": pob.group(2).strip(), "confidence": 0.8}

        # Registration / file number
        reg = re.search(
            r"(registration number|file number|state file number)\s*[:\-]?\s*([A-Za-z0-9\-]+)",
            text,
            re.IGNORECASE,
        )
        if reg:
            fields["registration_number"] = {"value": reg.group(2).strip(), "confidence": 0.8}

        # Date filed / registered
        filed = re.search(
            r"(date filed|date registered)\s*[:\-]?\s*([A-Za-z0-9\/\-\., ]+)",
            text,
            re.IGNORECASE,
        )
        if filed:
            normalized_date = normalize_date(filed.group(2).strip())
            if normalized_date:
                fields["date_filed"] = {"value": normalized_date, "confidence": 0.95}
            else:
                fields["date_filed"] = {"value": filed.group(2).strip(), "confidence": 0.8}

        # Informant
        inf = re.search(
            r"(informant)\s*[:\-]?\s*([A-Z ,.'\-]+)",
            text,
            re.IGNORECASE,
        )
        if inf:
            fields["informant"] = {"value": inf.group(2).strip(), "confidence": 0.8}

        # Registrar
        reg_name = re.search(
            r"(registrar|state registrar|local registrar)\s*[:\-]?\s*([A-Z ,.'\-]+)",
            text,
            re.IGNORECASE,
        )
        if reg_name:
            fields["registrar"] = {"value": reg_name.group(2).strip(), "confidence": 0.8}

        return fields

    @staticmethod
    def administrative_context(fields: dict) -> str:
        parts: list[str] = []

        parts.append(
            "A birth certificate is an official vital record used to document a person's birth "
            "for identity, citizenship, and administrative purposes."
        )

        if "registration_number" in fields:
            parts.append(
                "The registration or file number is used by the issuing authority to locate and verify the record."
            )

        if "date_filed" in fields:
            parts.append(
                "The date filed or registered indicates when the birth was officially recorded in the vital records system."
            )

        if "informant" in fields:
            parts.append(
                "The informant is the person who provided the information about the birth to the registrar."
            )

        if "registrar" in fields:
            parts.append(
                "The registrar's name and signature indicate official acceptance of the record into the vital statistics system."
            )

        return " ".join(parts)

    @staticmethod
    def historical_context(fields: dict) -> str:
        parts: list[str] = []

        parts.append(
            "Vital records systems, including birth certificates, developed as governments formalized population "
            "registration for public health, taxation, conscription, and civil administration."
        )

        if "registration_number" in fields:
            parts.append(
                "Registration numbers historically functioned as ledger identifiers within centralized record books."
            )

        if "date_filed" in fields:
            parts.append(
                "The distinction between the date of birth and the date filed reflects the administrative act of "
                "recording the event, separate from the event itself."
            )

        if "informant" in fields:
            parts.append(
                "The presence of an informant field highlights that the record is based on a sworn or attested statement "
                "by a reporting party, not an automatic recording."
            )

        return " ".join(parts)
