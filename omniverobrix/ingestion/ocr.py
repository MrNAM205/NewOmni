import sys
sys.modules['paddleocr'] = None
import subprocess

def try_tesseract(path: str) -> str:
    try:
        result = subprocess.run(
            ["tesseract", path, "stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        text = result.stdout.strip()
        return text if text else None
    except Exception:
        return None


def try_paddle(path: str) -> str:
    """
    Lazy-load PaddleOCR only if Tesseract fails AND PaddleOCR is installed.
    If paddlepaddle or paddleocr are missing, this fails silently.
    """
    try:
        from paddleocr import PaddleOCR
        ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')
        result = ocr_engine.ocr(path, cls=True)
        if not result:
            return None
        return "\n".join([line[1][0] for line in result[0]])
    except Exception:
        return None


def try_ocr(path: str) -> str:
    # First attempt: Tesseract
    text = try_tesseract(path)
    if text:
        return text

    # Second attempt: PaddleOCR (only if installed)
    return try_paddle(path)
