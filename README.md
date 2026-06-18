# Screenshot OCR Search

Search through months of screenshots as if they were searchable notes.

Screenshot OCR Search automatically watches your screenshot folder, extracts text using Tesseract OCR, stores the results in SQLite, and lets you instantly search screenshots you've taken days, weeks, or months ago.

---

## Features

* Automatic screenshot detection
* Real-time screenshot monitoring
* OCR text extraction using Tesseract
* SQLite-powered local storage
* Automatic backfill of missed screenshots
* Keyword search
* Search screenshots from today, this week, or this month
* Screenshot analytics and statistics
* Desktop GUI
* Configurable screenshot folder
* Fully local and privacy-friendly
* No cloud services or external APIs

---

## How It Works

```text
Take Screenshot
       ↓
Watcher detects new screenshot
       ↓
OCR extracts text
       ↓
Text stored in SQLite
       ↓
Search later through GUI
```

---

## Automatic Backfill

When the application starts, it automatically scans the configured screenshot folder and checks every screenshot against the database.

```text
Launch Application
       ↓
Backfill Runs
       ↓
Missing Screenshots Found
       ↓
OCR Performed
       ↓
Database Updated
       ↓
Real-Time Monitoring Starts
```

This ensures screenshots taken while the application was closed are automatically indexed the next time it launches.

Backfilled screenshots retain their original file timestamps, ensuring date-based searches remain accurate.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/nishchay-joshi/Screenshot-OCR.git
cd ScreenshotOCR
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Tesseract OCR

Install Tesseract OCR on your system.

If Tesseract is not available in PATH, configure the executable location inside:

```text
src/add.py
```

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

## Configuration

Create a `config.json` file in the project root:

```json
{
    "screenshot_folder": "C:/Users/YourName/Pictures/Screenshots"
}
```

Replace the path with the folder where screenshots are automatically saved on your system.

---

## Launch Application

```bash
python -m gui.app
```

Launching the GUI will automatically:

* Start the screenshot watcher
* Run backfill
* Begin real-time monitoring
* Open the search interface

No separate terminal or watcher process is required.

---

## Searching

### Keyword Search

Enter a keyword into the search bar:

```text
postgres
```

Example result:

```text
Screenshot_123.png
2026-06-18

...docker compose postgres restart command...
```

### Today's Screenshots

Click:

```text
Today
```

### Last Week

Click:

```text
Week
```

### Last Month

Click:

```text
Month
```

---

## Statistics

Click:

```text
Statistics
```

View:

* Total screenshots indexed
* OCR character count
* Estimated OCR word count
* Oldest screenshot
* Newest screenshot
* Database size
* Most common OCR terms

---

## Manual Backfill

Click:

```text
Backfill
```

to manually scan the screenshot folder and index any screenshots that are not yet present in the database.

Example:

```text
Running backfill...

✓ Indexed: Screenshot_431.png
✓ Indexed: Screenshot_432.png
✓ Indexed: Screenshot_433.png

Backfill complete. Indexed 3 file(s).
```

---

## Opening Screenshots

Search results are displayed as interactive cards.

```text
📄 Screenshot_123.png
📅 2026-06-18
🔗 Double-click to open screenshot
```

Double-click any result card to open the original screenshot.

---

## Project Structure

```text
ScreenshotOCR/
│
├── gui/
│   ├── __init__.py
│   └── app.py
│
├── src/
│   ├── __init__.py
│   ├── add.py
│   ├── config.py
│   ├── db.py
│   ├── search.py
│   ├── stats.py
│   └── watch.py
│
├── config.json
├── db.sqlite
├── README.md
└── requirements.txt
```
