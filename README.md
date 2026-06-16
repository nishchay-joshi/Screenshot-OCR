# Screenshot OCR Search

Search through months of screenshots as if they were searchable notes.

Screenshot OCR Search watches your screenshot folder, extracts text from screenshots using Tesseract OCR, stores the results in SQLite, and lets you search through them later.

## Features

* Automatic screenshot detection
* OCR text extraction using Tesseract
* SQLite database storage
* Automatic backfill of missed screenshots
* Keyword search
* Search screenshots from today, this week, or this month
* Configurable screenshot folder
* Runs completely locally
* No cloud services required

---

## How It Works

```text
Take Screenshot
       ↓
File appears in screenshot folder
       ↓
watch.py detects new file
       ↓
Tesseract extracts text
       ↓
Text stored in SQLite
       ↓
Search later using search.py
```

---

## Automatic Backfill

The watcher does more than just monitor new screenshots.

When `watch.py` starts, it first scans the configured screenshot folder and checks every screenshot against the database.

```text
Start watch.py
       ↓
Scan screenshot folder
       ↓
Find screenshots not in database
       ↓
OCR and index them
       ↓
Start live monitoring
```

This means screenshots taken while the application was not running are automatically indexed the next time the watcher starts.

Example:

```text
Take screenshots for a week
       ↓
Watcher is not running
       ↓
Start watch.py
       ↓
Missing screenshots are detected
       ↓
OCR is performed
       ↓
Database is updated
```

Backfilled screenshots retain their original file timestamps, allowing date-based searches such as `--today`, `--week`, and `--month` to remain accurate.

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

If Tesseract is not available in PATH, configure the executable location inside `add.py`:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

## Configuration

Create a `config.json` file:

```json
{
    "screenshot_folder": "C:/Users/YourName/Pictures/Screenshots"
}
```

Replace the path with the folder where screenshots are automatically saved on your system.

---

## Start Monitoring

```bash
python watch.py
```

Example output:

```text
Running backfill...

Backfill complete. Indexed 12 file(s).

Watching: C:\Users\YourName\Pictures\Screenshots
```

Keep this process running in the background.

Every new screenshot will be automatically indexed.

---

## Searching

### Keyword Search

```bash
python search.py postgres
```

Example:

```text
Found 3 result(s):

2025-06-16 18:22:51 | Screenshot_001.png
2025-06-15 11:09:13 | Screenshot_002.png
2025-06-12 09:34:51 | Screenshot_003.png
```

### Today's Screenshots

```bash
python search.py --today
```

### Last Week

```bash
python search.py --week
```

### Last Month

```bash
python search.py --month
```

---

## Project Structure

```text
.
├── add.py
├── db.py
├── init_db.py
├── search.py
├── watch.py
├── config.json
├── requirements.txt
└── db.sqlite
```
