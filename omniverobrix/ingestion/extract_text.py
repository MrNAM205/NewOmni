import os
import io
import pdfminer.high_level
from docx import Document
from PIL import Image
from omniverobrix.ingestion.ocr import try_ocr


# ---------------------------------------------------------
# SAFE TEXT DECODING
# ---------------------------------------------------------
def safe_read_text(path: str) -> str:
    """
    Safely read plain-text files using UTF-8 with fallback.
    Never throws UnicodeDecodeError.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception:
            return ""


# ---------------------------------------------------------
# PDF EXTRACTION
# ---------------------------------------------------------
def extract_pdf(path: str) -> str:
    try:
        output = io.StringIO()
        pdfminer.high_level.extract_text_to_fp(
            open(path, "rb"),
            output,
            laparams=None
        )
        text = output.getvalue().strip()
        if text:
            return text
    except Exception:
        pass
    return ""


# ---------------------------------------------------------
# DOCX EXTRACTION
# ---------------------------------------------------------
def extract_docx(path: str) -> str:
    try:
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs]).strip()
    except Exception:
        return ""


# ---------------------------------------------------------
# IMAGE EXTRACTION (OCR)
# ---------------------------------------------------------
def extract_image(path: str) -> str:
    try:
        img = Image.open(path)
        return try_ocr(path) or ""
    except Exception:
        return ""


# ---------------------------------------------------------
# UNIVERSAL EXTRACTOR
# ---------------------------------------------------------
def extract_text_from_file(path: str) -> str:
    """
    Pure-Python universal extractor.
    No textract. No subprocess. No encoding crashes.
    """
    ext = os.path.splitext(path)[1].lower()

    # TEXT-LIKE FILES
    if ext in [".txt", ".md", ".html", ".htm", ".csv", ".json", ".xml"]:
        return safe_read_text(path)

    # PDF
    if ext == ".pdf":
        text = extract_pdf(path)
        if text:
            return text
        # fallback to OCR
        return try_ocr(path) or ""

    # DOCX
    if ext == ".docx":
        return extract_docx(path)

    # IMAGES
    if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif", ".webp"]:
        return extract_image(path)

    # UNKNOWN → try text read → fallback to OCR
    text = safe_read_text(path)
    if text:
        return text

    return try_ocr(path) or ""