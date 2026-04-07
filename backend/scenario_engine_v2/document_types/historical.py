import re
from .base import DocumentAnalyzer
from .utils import normalize_date


class HistoricalDocumentAnalyzer(DocumentAnalyzer):
    """
    Analyzer for legacy / historical administrative documents.
    Focuses on:
      - registrar / informant / filed / seal patterns
      - older certificate / record language
      - explaining archival context without legal advice
    """

    @staticmethod
    def detect(text: str) -> bool:
        t = text.lower()

        keywords = [
            "registrar",
            "local registrar",
            "state registrar",
            "informant",
            "filed for record",
            "recorded in book",
            "volume",
            "folio",
            "seal",
            "this certifies that",
            "be it known",
            "know all men by these presents",
            "county clerk",
            "recorder of deeds",
            "register of deeds",
        ]

        return any(k in t for k in keywords)

    @staticmethod
    def extract_fields(text: str) -> dict:
        fields: dict[str, dict] = {}

        # Generic registration / file number
        reg = re.search(
            r"(registration number|file number|record number|book and page)\s*[:\-]?\s*([A-Za-z0-9\-\/ ]+)",
            text,
            re.IGNORECASE,
        )
        if reg:
            fields["registration_reference"] = {"value": reg.group(2).strip(), "confidence": 0.8}

        # Book / volume / page references
        book = re.search(
            r"(book|volume)\s*[:\-]?\s*([A-Za-z0-9\-\/ ]+)",
            text,
            re.IGNORECASE,
        )
        if book:
            fields["book_or_volume"] = {"value": book.group(2).strip(), "confidence": 0.8}

        page = re.search(
            r"(page|folio)\s*[:\-]?\s*([A-Za-z0-9\-\/ ]+)",
            text,
            re.IGNORECASE,
        )
        if page:
            fields["page_or_folio"] = {"value": page.group(2).strip(), "confidence": 0.8}

        # Filed / recorded date
        filed = re.search(
            r"FILED FOR RECORD:\s*([^\n]+)",
            text,
            re.IGNORECASE,
        )
        if filed:
            normalized_date = normalize_date(filed.group(1).strip())
            if normalized_date:
                fields["date_recorded"] = {"value": normalized_date, "confidence": 0.95}
            else:
                fields["date_recorded"] = {"value": filed.group(1).strip(), "confidence": 0.8}
        else:
            # Fallback for other date formats if needed
            filed = re.search(
                r"(recorded|date filed)\s*[:\-]?\s*([A-Za-z0-9\/\-\., ]+)",
                text,
                re.IGNORECASE,
            )
            if filed:
                normalized_date = normalize_date(filed.group(2).strip())
                if normalized_date:
                    fields["date_recorded"] = {"value": normalized_date, "confidence": 0.95}
                else:
                    fields["date_recorded"] = {"value": filed.group(2).strip(), "confidence": 0.8}

        # Clerk / registrar / recorder
        clerk = re.search(
            r"(county clerk|clerk of court|recorder of deeds|register of deeds|registrar)\s*[:\-]?\s*([A-Z ,.'\-]+)",
            text,
            re.IGNORECASE,
        )
        if clerk:
            fields["recording_officer"] = {"value": clerk.group(2).strip(), "confidence": 0.8}

        # Seal presence
        if re.search(r"(seal)", text, re.IGNORECASE):
            fields["seal_present"] = {"value": "true", "confidence": 0.7}

        return fields

    @staticmethod
    def administrative_context(fields: dict) -> str:
        parts: list[str] = []

        parts.append(
            "This document appears to follow a historical or legacy administrative format, "
            "where events or instruments were recorded in bound volumes or ledgers."
        )

        if "registration_reference" in fields:
            parts.append(
                "The registration or record reference identifies where this entry appears in the official books."
            )

        if "book_or_volume" in fields or "page_or_folio" in fields:
            parts.append(
                "Book, volume, page, or folio references indicate the physical location of the record in archival ledgers."
            )

        if "date_recorded" in fields:
            parts.append(
                "The recorded or filed date reflects when the document was accepted into the official record, "
                "which may differ from the date of the underlying event."
            )

        if "recording_officer" in fields:
            parts.append(
                "The named clerk, registrar, or recorder indicates the official responsible for maintaining the record."
            )

        if fields.get("seal_present") == "true":
            parts.append(
                "The presence of a seal suggests formal authentication by the issuing office."
            )

        return " ".join(parts)

    @staticmethod
    def historical_context(fields: dict) -> str:
        parts: list[str] = []

        parts.append(
            "Historically, administrative records were maintained in physical books, with each entry assigned "
            "a book, volume, and page or folio reference for retrieval."
        )

        if "registration_reference" in fields:
            parts.append(
                "Registration or record numbers functioned as index keys into these bound volumes."
            )

        if "date_recorded" in fields:
            parts.append(
                "The gap between the event date and the recorded date often reflects delays in reporting, "
                "travel, or administrative processing."
            )

        if "recording_officer" in fields:
            parts.append(
                "Named clerks and registrars historically served as custodians of local or county records, "
                "ensuring continuity of the archive."
            )

        if fields.get("seal_present") == "true":
            parts.append(
                "Seals were used to signify authenticity and authority in an era before digital signatures."
            )

        return " ".join(parts)
