from datetime import datetime, timedelta
import sys

from src.db import get_connection


def search_text(term):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT path, screenshot_date
        FROM screenshots
        WHERE lower(extracted_text)
        LIKE lower(?)
        ORDER BY screenshot_date DESC
        """,
        (f"%{term}%",),
    ).fetchall()

    conn.close()

    return rows


def search_since(days):

    cutoff = (
        datetime.now() - timedelta(days=days)
    ).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT path, screenshot_date
        FROM screenshots
        WHERE screenshot_date >= ?
        ORDER BY screenshot_date DESC
        """,
        (cutoff,),
    ).fetchall()

    conn.close()

    return rows


def print_results(results):

    if not results:
        print("\nNo matches found.\n")
        return

    print(f"\nFound {len(results)} result(s):\n")

    for i, (path, date) in enumerate(
        results,
        start=1,
    ):
        filename = path.split("\\")[-1]

        print(
            f"[{i}] {date} | {filename}"
        )


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            """
python -m src.search keyword
python -m src.search --today
python -m src.search --week
python -m src.search --month
"""
        )
        sys.exit()

    arg = sys.argv[1]

    if arg == "--today":
        results = search_since(1)

    elif arg == "--week":
        results = search_since(7)

    elif arg == "--month":
        results = search_since(30)

    else:
        results = search_text(arg)

    print_results(results)