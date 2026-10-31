from pathlib import Path

from PySide6.QtCore import QStandardPaths


def app_data_directory() -> Path:
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
    directory = Path(location)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def history_file() -> Path:
    return app_data_directory() / "history.json"


def browser_storage_directory() -> Path:
    return app_data_directory() / "browser"


def partial_downloads_directory() -> Path:
    return app_data_directory() / "partial"
