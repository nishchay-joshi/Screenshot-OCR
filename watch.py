from pathlib import Path
import json
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from add import index_image
from db import screenshot_exists


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
            print(f"Error: {e}")


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

            print(f"Failed: {path.name}")
            print(e)

    print(f"\nBackfill complete. Indexed {count} file(s).\n")


def main():

    with open("config.json") as f:
        config = json.load(f)

    screenshot_folder = Path(
        config["screenshot_folder"]
    )

    if not screenshot_folder.exists():
        raise FileNotFoundError(
            f"Folder not found: {screenshot_folder}"
        )

    backfill(screenshot_folder)

    observer = Observer()

    observer.schedule(
        ScreenshotHandler(),
        str(screenshot_folder),
        recursive=False,
    )

    observer.start()

    print(
        f"Watching: {screenshot_folder.resolve()}"
    )

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()