from datetime import datetime, timedelta
import sys

from src.db import get_connection


def generate_snippet(text, query, radius=40):

    text_lower = text.lower()
    query_lower = query.lower()

    position = text_lower.find(query_lower)

    if position == -1:

        snippet = text[:80]

        if len(text) > 80:
            snippet += "..."

        return snippet.replace("\n", " ")

    start = max(0, position - radius)
    end = min(
        len(text),
        position + len(query) + radius
    )

    snippet = text[start:end]
    snippet = snippet.replace("\n", " ")

    return f"...{snippet}..."


def search_text(term):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            path,
            screenshot_date,
            extracted_text
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


def print_results(results, query=None):

    if not results:
        print("\nNo matches found.\n")
        return

    print(
        f"\nFound {len(results)} result(s):\n"
    )

    for i, row in enumerate(results, start=1):
        if len(row) == 3:
            path, date, text = row
        else:
            path, date = row
            text = ""

        filename = path.split("\\")[-1]

        print(f"[{i}] {date} | {filename}")

        if query and text:
            snippet = generate_snippet(
                text,
                query,
            )

            print(f"    {snippet}")


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

    if arg.startswith("--"):
        print_results(results)
    else:
        print_results(
            results,
            query=arg,
        )