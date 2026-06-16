import sys
from datetime import datetime, timedelta

from db import get_connection


def search_text(term):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT path, created_at
        FROM screenshots
        WHERE lower(extracted_text)
        LIKE lower(?)
        ORDER BY created_at DESC
        """,
        (f"%{term}%",),
    ).fetchall()

    conn.close()

    return rows


def search_since(days):
    conn = get_connection()

    cutoff = (
        datetime.now() - timedelta(days=days)
    ).strftime("%Y-%m-%d %H:%M:%S")

    rows = conn.execute(
        """
        SELECT path, created_at
        FROM screenshots
        WHERE created_at >= ?
        ORDER BY created_at DESC
        """,
        (cutoff,),
    ).fetchall()

    conn.close()

    return rows


def print_results(results):

    if not results:
        print("No matches found.")
        return

    print(f"\nFound {len(results)} result(s):\n")

    for path, created_at in results:
        print(f"{created_at} | {path}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("""
Usage:

python search.py keyword

python search.py --today

python search.py --week

python search.py --month
        """)
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