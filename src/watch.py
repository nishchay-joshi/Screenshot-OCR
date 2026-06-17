from pathlib import Path
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.add import index_image
from src.db import (
    screenshot_exists,
    create_tables,
)
from src.config import get_config


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp",
}


class ScreenshotHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        path = Path(event.src_path)

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return

        try:

            time.sleep(1)

            full_path = str(path.resolve())

            if screenshot_exists(full_path):
                return

            print(f"Detected: {path.name}")

            index_image(path)

        except Exception as e:
            print(e)


def backfill(folder):

    print("\nRunning backfill...\n")

    count = 0

    for path in folder.iterdir():

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        full_path = str(path.resolve())

        if screenshot_exists(full_path):
            continue

        try:

            index_image(path)

            count += 1

        except Exception as e:

            print(e)

    print(
        f"\nBackfill complete. Indexed {count} file(s).\n"
    )


def main():

    create_tables()

    config = get_config()

    screenshot_folder = Path(
        config["screenshot_folder"]
    )

    backfill(screenshot_folder)

    observer = Observer()

    observer.schedule(
        ScreenshotHandler(),
        str(screenshot_folder),
        recursive=False,
    )

    observer.start()

    print(f"Watching: {screenshot_folder}")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()