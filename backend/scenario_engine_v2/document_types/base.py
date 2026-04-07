class DocumentAnalyzer:
    """
    Abstract base class for all document analyzers.
    Each analyzer must implement:
      - detect(text)
      - extract_fields(text)
      - administrative_context(fields)
      - historical_context(fields)
    """

    @staticmethod
    def detect(text: str) -> bool:
        raise NotImplementedError

    @staticmethod
    def extract_fields(text: str) -> dict:
        raise NotImplementedError

    @staticmethod
    def administrative_context(fields: dict) -> str:
        return ""

    @staticmethod
    def historical_context(fields: dict) -> str:
        return ""
