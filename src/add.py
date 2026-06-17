from pathlib import Path
from datetime import datetime

import pytesseract
from PIL import Image

from src.db import get_connection

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text


def index_image(image_path):
    image_path = str(Path(image_path).resolve())

    text = extract_text(image_path)

    screenshot_date = datetime.fromtimestamp(
        Path(image_path).stat().st_mtime
    )

    conn = get_connection()

    conn.execute(
        """
        INSERT OR REPLACE INTO screenshots
        (path, extracted_text, screenshot_date)
        VALUES (?, ?, ?)
        """,
        (image_path, text, screenshot_date),
    )

    conn.commit()
    conn.close()

    print(f"Indexed: {image_path}")

