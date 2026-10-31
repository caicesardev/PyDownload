import shutil
import time
from enum import Enum, auto
from pathlib import Path
from typing import Any

import yt_dlp
from PySide6.QtCore import QThread, Signal
from yt_dlp.utils import DownloadCancelled, YoutubeDLError

from src.models.download_request import DownloadRequest
from src.services.ydl_options import describe_error
from src.utils.formatting import format_bytes, format_duration

OUTPUT_TEMPLATE = "%(title)s.%(ext)s"
NO_CODEC = "none"
PROGRESS_EMIT_INTERVAL_SECONDS = 0.25
POSTPROCESSOR_MESSAGES = {
    "Merger": "Uniendo vídeo y audio…",
    "ExtractAudio": "Convirtiendo audio…",
    "MoveFilesAfterDownload": "Moviendo a la carpeta de descargas…",
}
DEFAULT_POSTPROCESSOR_MESSAGE = "Finalizando…"


class Interruption(Enum):
    PAUSE = auto()
    CANCEL = auto()


class DownloadWorker(QThread):
    progress_changed = Signal(int, float, str)
    phase_changed = Signal(int, str, bool)
    completed = Signal(int, str)
    failed = Signal(int, str)
    paused = Signal(int)
    cancelled = Signal(int)

    def __init__(
        self,
        job_id: int,
        request: DownloadRequest,
        ydl_options: dict[str, Any],
        temp_directory: Path,
    ) -> None:
        super().__init__()
        self.job_id = job_id
        self._request = request
        self._ydl_options = ydl_options
        self._temp_directory = temp_directory
        self._interruption: Interruption | None = None
        self._last_progress_emit = 0.0

    def request_pause(self) -> None:
        self._interruption = Interruption.PAUSE

    def request_cancel(self) -> None:
        self._interruption = Interruption.CANCEL

    def run(self) -> None:
        try:
            self._prepare_directories()
            with yt_dlp.YoutubeDL(self._download_options()) as ydl:
                info = ydl.extract_info(self._request.url, download=True)
        except DownloadCancelled:
            self._finish_interrupted()
            return
        except YoutubeDLError as error:
            self.failed.emit(self.job_id, describe_error(error))
            return
        except OSError as error:
            self.failed.emit(self.job_id, f"No se pudo escribir en disco: {error.strerror or error}")
            return
        shutil.rmtree(self._temp_directory, ignore_errors=True)
        self.completed.emit(self.job_id, self._final_filepath(info))

    def _prepare_directories(self) -> None:
        self._request.destination.mkdir(parents=True, exist_ok=True)
        self._temp_directory.mkdir(parents=True, exist_ok=True)

    def _download_options(self) -> dict[str, Any]:
        return {
            **self._ydl_options,
            **self._request.ydl_options(),
            "paths": {"home": str(self._request.destination), "temp": str(self._temp_directory)},
            "outtmpl": OUTPUT_TEMPLATE,
            "progress_hooks": [self._on_progress],
            "postprocessor_hooks": [self._on_postprocessing],
        }

    def _finish_interrupted(self) -> None:
        if self._interruption is Interruption.PAUSE:
            self.paused.emit(self.job_id)
            return
        shutil.rmtree(self._temp_directory, ignore_errors=True)
        self.cancelled.emit(self.job_id)

    def _on_progress(self, progress: dict[str, Any]) -> None:
        if self._interruption is not None:
            raise DownloadCancelled()
        if progress["status"] != "downloading" or not self._should_emit_progress():
            return
        total_bytes = progress.get("total_bytes") or progress.get("total_bytes_estimate")
        downloaded_bytes = progress.get("downloaded_bytes") or 0
        percent = downloaded_bytes * 100 / total_bytes if total_bytes else 0.0
        self.progress_changed.emit(self.job_id, percent, self._describe_progress(progress, total_bytes))

    def _should_emit_progress(self) -> bool:
        now = time.monotonic()
        if now - self._last_progress_emit < PROGRESS_EMIT_INTERVAL_SECONDS:
            return False
        self._last_progress_emit = now
        return True

    def _on_postprocessing(self, progress: dict[str, Any]) -> None:
        if progress["status"] == "started":
            message = POSTPROCESSOR_MESSAGES.get(progress["postprocessor"], DEFAULT_POSTPROCESSOR_MESSAGE)
            self.phase_changed.emit(self.job_id, message, False)

    @staticmethod
    def _describe_progress(progress: dict[str, Any], total_bytes: float | None) -> str:
        stream = progress.get("info_dict", {})
        stream_kind = "Vídeo" if stream.get("vcodec", NO_CODEC) != NO_CODEC else "Audio"
        downloaded = format_bytes(progress.get("downloaded_bytes") or 0)
        details = [stream_kind, f"{downloaded} de {format_bytes(total_bytes)}" if total_bytes else downloaded]
        if speed := progress.get("speed"):
            details.append(f"{format_bytes(speed)}/s")
        if eta := progress.get("eta"):
            details.append(f"quedan {format_duration(eta)}")
        return " · ".join(details)

    @staticmethod
    def _final_filepath(info: dict[str, Any]) -> str:
        downloads = info.get("requested_downloads") or [{}]
        return downloads[-1].get("filepath", "")
