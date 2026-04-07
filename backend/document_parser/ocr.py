from PIL import Image
import pytesseract

def extract_ocr_text(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)
