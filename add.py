from pathlib import Path
from datetime import datetime

import pytesseract
from PIL import Image

from db import get_connection

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

    file_time = datetime.fromtimestamp(
        Path(image_path).stat().st_mtime
    )

    conn = get_connection()

    conn.execute(
        """
        INSERT OR REPLACE INTO screenshots
        (path, extracted_text, screenshot_date)
        VALUES (?, ?, ?)
        """,
        (image_path, text, file_time),
    )

    conn.commit()
    conn.close()

    print(f"Indexed: {image_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python add.py image.png")
        raise SystemExit

    index_image(sys.argv[1])