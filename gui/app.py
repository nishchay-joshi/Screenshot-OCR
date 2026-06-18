import os
import sys
import threading
from pathlib import Path

import customtkinter as ctk

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.search import (
    search_text,
    search_since,
    generate_snippet,
)

from src.stats import get_stats
from src.watch import run_backfill
from src.watch import main as start_watcher


class ScreenshotSearchApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Screenshot OCR Search")
        self.geometry("1100x750")

        self.results = []

        self.start_background_watcher()

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Screenshot OCR Search",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            pady=(20, 10)
        )

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=40,
            placeholder_text="Search screenshots..."
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.search_entry.bind(
            "<Return>",
            self.search_keyword
        )

        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            width=120,
            height=40,
            command=self.search_keyword
        )

        search_btn.pack(side="right")

        filter_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        filter_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkButton(
            filter_frame,
            text="Today",
            command=self.search_today
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            filter_frame,
            text="Week",
            command=self.search_week
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            filter_frame,
            text="Month",
            command=self.search_month
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            filter_frame,
            text="Statistics",
            command=self.show_stats
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            filter_frame,
            text="Backfill",
            command=self.run_backfill
        ).pack(
            side="left",
            padx=5
        )

        self.result_count = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )

        self.result_count.pack(
            fill="x",
            padx=25
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            self
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    def clear_results(self):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def start_background_watcher(self):

        watcher_thread = threading.Thread(
            target=self.run_watcher,
            daemon=True
        )

        watcher_thread.start()

    def run_watcher(self):

        try:

            start_watcher()

        except Exception as e:

            print(
                f"Watcher error: {e}"
            )

    def create_result_card(
            self,
            index,
            path,
            date,
            snippet=""
    ):

        card = ctk.CTkFrame(
            self.scroll_frame
        )

        card.pack(
            fill="x",
            padx=5,
            pady=8
        )

        NORMAL_COLOR = card.cget("fg_color")
        HOVER_COLOR = ("#3B3B3B", "#2B2B2B")

        filename = Path(path).name

        title = ctk.CTkLabel(
            card,
            text=f"📄 {filename}",
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=(10, 0)
        )

        date_label = ctk.CTkLabel(
            card,
            text=f"📅 {date}",
            anchor="w"
        )

        date_label.pack(
            anchor="w",
            padx=15
        )

        hint_label = ctk.CTkLabel(
            card,
            text="🔗 Double-click to open screenshot",
            anchor="w",
            font=("Segoe UI", 11)
        )

        hint_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 5)
        )

        if snippet:

            snippet_label = ctk.CTkLabel(
                card,
                text=snippet,
                justify="left",
                wraplength=900,
                anchor="w"
            )

            snippet_label.pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )

        def open_file(event=None):
            os.startfile(path)

        def on_enter(event):
            card.configure(
                fg_color=HOVER_COLOR
            )

        def on_leave(event):
            card.configure(
                fg_color=NORMAL_COLOR
            )

        clickable_widgets = [
            card,
            title,
            date_label,
            hint_label
        ]

        if snippet:
            clickable_widgets.append(
                snippet_label
            )

        for widget in clickable_widgets:

            widget.bind(
                "<Double-Button-1>",
                open_file
            )

            widget.bind(
                "<Enter>",
                on_enter
            )

            widget.bind(
                "<Leave>",
                on_leave
            )

            try:
                widget.configure(
                    cursor="hand2"
                )
            except Exception:
                pass

    def display_results(
        self,
        results,
        query=None
    ):

        self.clear_results()

        self.results = results

        self.result_count.configure(
            text=f"Found {len(results)} result(s)"
        )

        if not results:

            no_results = ctk.CTkLabel(
                self.scroll_frame,
                text="No results found."
            )

            no_results.pack(
                pady=20
            )

            return

        for i, row in enumerate(
            results,
            start=1
        ):

            if len(row) == 3:

                path, date, text = row

                snippet = ""

                if query:

                    snippet = generate_snippet(
                        text,
                        query
                    )

            else:

                path, date = row
                snippet = ""

            self.create_result_card(
                i,
                path,
                date,
                snippet
            )

    def search_keyword(
        self,
        event=None
    ):

        query = (
            self.search_entry
            .get()
            .strip()
        )

        if not query:
            return

        results = search_text(query)

        self.display_results(
            results,
            query=query
        )

    def search_today(self):

        self.display_results(
            search_since(1)
        )

    def search_week(self):

        self.display_results(
            search_since(7)
        )

    def search_month(self):

        self.display_results(
            search_since(30)
        )

    def show_stats(self):

        self.clear_results()

        stats = get_stats()

        self.result_count.configure(
            text="Statistics"
        )

        stats_card = ctk.CTkFrame(
            self.scroll_frame
        )

        stats_card.pack(
            fill="x",
            padx=5,
            pady=10
        )

        text = f"""
Indexed Screenshots : {stats['total_screenshots']}
Total OCR Characters: {stats['total_characters']:,}
Estimated OCR Words : {stats['estimated_words']:,}
Oldest Screenshot   : {stats['oldest']}
Newest Screenshot   : {stats['newest']}
Database Size       : {stats['db_size_mb']} MB

Top OCR Terms
------------------------------
"""

        for word, count in stats["top_words"]:
            text += f"{word:<20} {count}\n"

        label = ctk.CTkLabel(
            stats_card,
            text=text,
            justify="left",
            font=("Consolas", 15)
        )

        label.pack(
            padx=20,
            pady=20,
            anchor="w"
        )

    def run_backfill(self):

        self.clear_results()

        self.result_count.configure(
            text="Running Backfill..."
        )

        loading_card = ctk.CTkFrame(
            self.scroll_frame
        )

        loading_card.pack(
            fill="x",
            padx=5,
            pady=10
        )

        self.backfill_label = ctk.CTkLabel(
            loading_card,
            text="Scanning screenshots...",
            justify="left",
            font=("Consolas", 14)
        )

        self.backfill_label.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        thread = threading.Thread(
            target=self._backfill_worker,
            daemon=True
        )

        thread.start()

    def _backfill_worker(self):

        try:

            output = run_backfill()

            result_text = "\n".join(output)

            self.after(
                0,
                lambda: self._display_backfill_result(
                    result_text
                )
            )

        except Exception as e:

            self.after(
                0,
                lambda: self._display_backfill_result(
                    f"Backfill failed:\n\n{e}"
                )
            )

    def _display_backfill_result(
        self,
        text
    ):

        self.clear_results()

        self.result_count.configure(
            text="Backfill Results"
        )

        card = ctk.CTkFrame(
            self.scroll_frame
        )

        card.pack(
            fill="x",
            padx=5,
            pady=10
        )

        label = ctk.CTkLabel(
            card,
            text=text,
            justify="left",
            font=("Consolas", 14)
        )

        label.pack(
            anchor="w",
            padx=20,
            pady=20
        )


if __name__ == "__main__":

    ctk.set_appearance_mode("dark")

    app = ScreenshotSearchApp()

    app.mainloop()

