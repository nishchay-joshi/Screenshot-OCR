from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "db.sqlite"
CONFIG_PATH = PROJECT_ROOT / "config.json"


def get_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)