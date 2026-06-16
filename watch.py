from pathlib import Path
import time
import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from add import index_image


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

        print(f"Detected: {path.name}")

        try:
            time.sleep(1)

            index_image(path)

        except Exception as e:
            print(f"Error indexing {path}: {e}")


def main():

    with open("config.json") as f:
        config = json.load(f)

    screenshot_folder = Path(
        config["screenshot_folder"]
    )

    screenshot_folder.mkdir(exist_ok=True)

    observer = Observer()

    observer.schedule(
        ScreenshotHandler(),
        str(screenshot_folder),
        recursive=False,
    )

    observer.start()

    print(f"Watching folder: {screenshot_folder.resolve()}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()