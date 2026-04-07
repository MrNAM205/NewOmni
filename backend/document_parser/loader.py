import os
from .pdf import extract_pdf_text
from .ocr import extract_ocr_text

def load_document(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext in [".pdf"]:
        return extract_pdf_text(path)

    if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return extract_ocr_text(path)

    raise ValueError(f"Unsupported file type: {ext}")
