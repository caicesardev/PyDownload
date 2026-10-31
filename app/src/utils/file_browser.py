import sys
from pathlib import Path

from PySide6.QtCore import QDir, QProcess, QUrl
from PySide6.QtGui import QDesktopServices

WINDOWS_EXPLORER = "explorer.exe"


def reveal_in_file_manager(file_path: str) -> bool:
    path = Path(file_path)
    if path.is_dir():
        return open_directory(path)
    if path.is_file() and sys.platform == "win32":
        started, _process_id = QProcess.startDetached(WINDOWS_EXPLORER, [f"/select,{QDir.toNativeSeparators(str(path))}"])
        return started
    return open_directory(path.parent)


def open_directory(directory: Path) -> bool:
    return directory.is_dir() and QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory)))


def open_file(file_path: str) -> bool:
    path = Path(file_path)
    return path.is_file() and QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
