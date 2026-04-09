import subprocess
from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')

def try_tesseract(path: str) -> str:
    try:
        result = subprocess.run(
            ["tesseract", path, "stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def try_paddle(path: str) -> str:
    try:
        result = ocr_engine.ocr(path, cls=True)
        if not result:
            return None
        return "\n".join([line[1][0] for line in result[0]])
    except Exception:
        return None

def try_ocr(path: str) -> str:
    text = try_tesseract(path)
    if text:
        return text
    return try_paddle(path)