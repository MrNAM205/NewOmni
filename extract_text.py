import textract

def extract_text_from_file(path: str) -> str:
    try:
        text = textract.process(path)
        return text.decode("utf-8", errors="ignore")
    except Exception:
        return None