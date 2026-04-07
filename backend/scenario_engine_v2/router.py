# backend/scenario_engine_v2/router.py

from .classifier import classify_scenario
from .stages import identify_stage
from .actions import recommend_actions

# Import the new document type modules
from .document_types.billing import BillingStatementAnalyzer
from .document_types.remittance import RemittanceAnalyzer
from .document_types.vital_records import VitalRecordAnalyzer
from .document_types.historical import HistoricalDocumentAnalyzer

def detect_document_type(text: str) -> str:
    if BillingStatementAnalyzer.detect(text):
        return "billing"

    if RemittanceAnalyzer.detect(text):
        return "remittance"

    if VitalRecordAnalyzer.detect(text):
        return "vital_record"

    if HistoricalDocumentAnalyzer.detect(text):
        return "historical"

    return "unknown"


def analyze_document(document_type: str, text: str) -> dict:
    if document_type == "billing":
        fields = BillingStatementAnalyzer.extract_fields(text)
        return {
            "document_type": "billing",
            "fields": fields,
            "administrative_context": BillingStatementAnalyzer.administrative_context(fields),
            "historical_context": BillingStatementAnalyzer.historical_context(fields),
        }

    if document_type == "remittance":
        fields = RemittanceAnalyzer.extract_fields(text)
        ocr_line_info = RemittanceAnalyzer.extract_ocr_line(text)

        # merge OCR-line into fields if present
        fields.update(ocr_line_info)

        return {
            "document_type": "remittance",
            "fields": fields,
            "administrative_context": RemittanceAnalyzer.administrative_context(fields),
            "historical_context": RemittanceAnalyzer.historical_context(fields),
        }

    if document_type == "vital_record":
        fields = VitalRecordAnalyzer.extract_fields(text)
        return {
            "document_type": "vital_record",
            "fields": fields,
            "administrative_context": VitalRecordAnalyzer.administrative_context(fields),
            "historical_context": VitalRecordAnalyzer.historical_context(fields),
        }

    if document_type == "historical":
        fields = HistoricalDocumentAnalyzer.extract_fields(text)
        return {
            "document_type": "historical",
            "fields": fields,
            "administrative_context": HistoricalDocumentAnalyzer.administrative_context(fields),
            "historical_context": HistoricalDocumentAnalyzer.historical_context(fields),
        }

    return {
        "document_type": "unknown",
        "fields": {},
        "administrative_context": "",
        "historical_context": "",
    }


def run_scenario_engine(text: str) -> dict:
    """
    Main entry point for Scenario Engine v2.
    Combines:
      - scenario classification
      - stage identification
      - recommended actions
      - document type detection
      - document analysis
    """

    scenario = classify_scenario(text)
    stage = identify_stage(scenario, text)
    actions = recommend_actions(scenario, stage)

    document_type = detect_document_type(text)
    document_info = analyze_document(document_type, text)

    return {
        "scenario": scenario,
        "stage": stage,
        "actions": actions,
        "document": document_info
    }
