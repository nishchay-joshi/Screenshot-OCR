# Screenshot OCR Search

A lightweight Python tool that automatically indexes screenshots using OCR and lets you search through them later.

## Features

* Automatic screenshot detection
* OCR text extraction using Tesseract
* SQLite database storage
* Keyword search
* Search screenshots from today, this week, or this month
* Configurable screenshot folder via `config.json`
* Runs locally
* No cloud services required

---

## How It Works

```text
Take Screenshot
       ↓
File appears in configured screenshot folder
       ↓
watch.py detects new file
       ↓
Tesseract extracts text
       ↓
Text stored in SQLite
       ↓
Search later using search.py
```

Example:

You take a screenshot of:

```text
PostgreSQL connection string
Host: localhost
User: admin
```

Weeks later:

```bash
python search.py postgres
```

Result:

```text
2026-06-16 18:22:51 | Screenshot_20260616.png
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/nishchay-joshi/Screenshot-OCR.git
cd screenshot-ocr-search
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

Windows users may need to configure:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

inside `add.py` if Tesseract is not available in PATH.

---

## Configuration

Create a `config.json` file:

```json
{
    "screenshot_folder": "C:/Users/YourName/Pictures/Screenshots"
}
```

Replace the path with the folder where your screenshots are automatically saved.

---

## Initialize Database

Run once:

```bash
python init_db.py
```

Creates:

```text
db.sqlite
```

---

## Start Monitoring

```bash
python watch.py
```

Expected output:

```text
Watching: C:\Users\YourName\Pictures\Screenshots
```

Keep this process running.

Every new screenshot that appears in the configured folder will be automatically indexed.

---

## Searching

### Keyword Search

```bash
python search.py postgres
```

Example:

```text
2026-06-16 20:11:31 | Screenshot_20260616.png
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
