# Screenshot OCR Search

Search through months of screenshots as if they were searchable notes.

Screenshot OCR Search automatically watches your screenshot folder, extracts text using Tesseract OCR, stores the results in SQLite, and lets you instantly search through screenshots you've taken days, weeks, or months ago.

---

## Features

* Automatic screenshot detection
* OCR text extraction with Tesseract
* SQLite-powered local storage
* Automatic backfill of missed screenshots
* Keyword-based screenshot search
* Date-based filtering (`--today`, `--week`, `--month`)
* Screenshot analytics and statistics
* Configurable screenshot directory
* Fully local and privacy-friendly
* No cloud services or external APIs

---

## How It Works

```text
Take Screenshot
       ↓
File appears in screenshot folder
       ↓
Watcher detects new file
       ↓
OCR extracts text
       ↓
Text stored in SQLite
       ↓
Search screenshots later
```

---

## Automatic Backfill

The application does more than monitor new screenshots.

Whenever the watcher starts, it scans the configured screenshot directory and checks every screenshot against the database.

```text
Start Watcher
       ↓
Scan Screenshot Folder
       ↓
Find Missing Screenshots
       ↓
Run OCR
       ↓
Update Database
       ↓
Begin Live Monitoring
```

This ensures screenshots taken while the application was not running are automatically indexed the next time it starts.

Example:

```text
Take screenshots for a week
       ↓
Application is not running
       ↓
Start watcher
       ↓
Missed screenshots detected
       ↓
OCR performed automatically
       ↓
Database updated
```

Backfilled screenshots retain their original file timestamps, ensuring date-based searches remain accurate.

Example startup output:

```text
Running backfill...

Indexed: Screenshot (263).png
Indexed: Screenshot (264).png
Indexed: Screenshot 2026-06-16 214351.png
Indexed: Screenshot 2026-06-16 220045.png

Backfill complete. Indexed 4 file(s).

Watching: C:\Users\YourName\Pictures\Screenshots
```

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

If Tesseract is not available in PATH, configure the executable location inside `src/add.py`:

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

Replace the path with the directory where screenshots are automatically saved on your system.

---

## Start Monitoring

```bash
python -m src.watch
```

The watcher will:

1. Create database tables if needed
2. Backfill any missing screenshots
3. Begin monitoring for new screenshots

---

## Searching

### Keyword Search

```bash
python -m src.search postgres
```

Example output:

```text
Found 3 result(s):

[1] 2025-06-16 18:22:51 | Screenshot_001.png
[2] 2025-06-15 11:09:13 | Screenshot_002.png
[3] 2025-06-12 09:34:51 | Screenshot_003.png
```

### Today's Screenshots

```bash
python -m src.search --today
```

### Last Week

```bash
python -m src.search --week
```

### Last Month

```bash
python -m src.search --month
```

---

## Analytics

View statistics about your screenshot archive:

```bash
python -m src.stats
```

Example output:

```text
Screenshot OCR Statistics

----------------------------------------
Indexed Screenshots : 412
Total OCR Characters: 1,248,941
Estimated OCR Words : 248,771
Oldest Screenshot   : 2025-03-11 08:21:14
Newest Screenshot   : 2026-06-17 09:14:32
Database Size       : 18.73 MB

Top OCR Terms
----------------------------------------
docker               184
postgres             127
kubernetes           91
react                82
python               76
----------------------------------------
```

---

## Project Structure

```text
ScreenshotOCR/
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
