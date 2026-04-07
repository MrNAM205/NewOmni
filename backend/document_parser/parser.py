from .loader import load_document

def parse_document(path: str) -> str:
    """
    Loads a document (PDF or image) and returns clean text.
    """
    raw = load_document(path)

    # Basic cleanup
    cleaned = raw.replace("", "").strip()

    return cleaned
