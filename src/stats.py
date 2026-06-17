from pathlib import Path
from collections import Counter
import re

from src.db import get_connection
from src.config import DB_PATH


STOP_WORDS = {
    "this", "that", "with", "from", "have",
    "your", "into", "when", "where", "what",
    "which", "there", "their", "about",
    "would", "could", "should", "been",
    "were", "them", "they", "then", "than",
    "also", "just", "some", "such", "will",
    "using", "used", "user", "users", "a", "the"
}


def get_stats():

    conn = get_connection()

    total_screenshots = conn.execute(
        """
        SELECT COUNT(*)
        FROM screenshots
        """
    ).fetchone()[0]

    total_characters = conn.execute(
        """
        SELECT COALESCE(SUM(LENGTH(extracted_text)), 0)
        FROM screenshots
        """
    ).fetchone()[0]

    oldest = conn.execute(
        """
        SELECT screenshot_date
        FROM screenshots
        ORDER BY screenshot_date ASC
        LIMIT 1
        """
    ).fetchone()

    newest = conn.execute(
        """
        SELECT screenshot_date
        FROM screenshots
        ORDER BY screenshot_date DESC
        LIMIT 1
        """
    ).fetchone()

    all_text = conn.execute(
        """
        SELECT extracted_text
        FROM screenshots
        """
    ).fetchall()

    conn.close()

    words = []

    for row in all_text:

        text = row[0]

        if not text:
            continue

        extracted_words = re.findall(
            r"\b[a-zA-Z]{4,}\b",
            text.lower()
        )

        for word in extracted_words:

            if word not in STOP_WORDS:
                words.append(word)

    estimated_words = len(words)

    word_counter = Counter(words)

    top_words = word_counter.most_common(10)

    db_size_mb = (
            DB_PATH.stat().st_size
            / (1024 * 1024)
    )

    return {
        "total_screenshots": total_screenshots,
        "total_characters": total_characters,
        "estimated_words": estimated_words,
        "oldest": oldest[0] if oldest else "N/A",
        "newest": newest[0] if newest else "N/A",
        "db_size_mb": round(db_size_mb, 2),
        "top_words": top_words,
    }


def print_stats():

    stats = get_stats()

    print("\nScreenshot OCR Statistics\n")

    print("-" * 40)

    print(
        f"Indexed Screenshots : {stats['total_screenshots']}"
    )

    print(
        f"Total OCR Characters: {stats['total_characters']:,}"
    )

    print(
        f"Estimated OCR Words : {stats['estimated_words']:,}"
    )

    print(
        f"Oldest Screenshot   : {stats['oldest']}"
    )

    print(
        f"Newest Screenshot   : {stats['newest']}"
    )

    print(
        f"Database Size       : {stats['db_size_mb']} MB"
    )

    print("\nTop OCR Terms")

    print("-" * 40)

    for word, count in stats["top_words"]:

        print(
            f"{word:<20} {count}"
        )

    print("-" * 40)


if __name__ == "__main__":
    print_stats()