from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from src.models.download_request import DownloadRequest


class DownloadState(Enum):
    QUEUED = "En cola"
    RUNNING = "Descargando"
    PAUSING = "Pausando…"
    PAUSED = "En pausa"
    CANCELLING = "Cancelando…"
    COMPLETED = "Completada"
    FAILED = "Error"
    CANCELLED = "Cancelada"

    @property
    def label(self) -> str:
        return self.value


ACTIVE_STATES = frozenset({DownloadState.RUNNING, DownloadState.PAUSING, DownloadState.CANCELLING})
FINISHED_STATES = frozenset({DownloadState.COMPLETED, DownloadState.FAILED, DownloadState.CANCELLED})
PENDING_STATES = frozenset({DownloadState.QUEUED, DownloadState.PAUSED}) | ACTIVE_STATES


@dataclass
class DownloadJob:
    job_id: int
    request: DownloadRequest
    title: str
    thumbnail_url: str
    temp_directory: Path
    state: DownloadState = DownloadState.QUEUED
    progress: float = 0.0
    detail: str = ""
    filepath: str = ""
    error: str = ""
    cancellable: bool = field(default=True)

    @property
    def is_active(self) -> bool:
        return self.state in ACTIVE_STATES

    @property
    def is_pending(self) -> bool:
        return self.state in PENDING_STATES

    @property
    def is_finished(self) -> bool:
        return self.state in FINISHED_STATES

    @property
    def can_pause(self) -> bool:
        return self.state in (DownloadState.QUEUED, DownloadState.RUNNING) and self.cancellable

    @property
    def can_resume(self) -> bool:
        return self.state is DownloadState.PAUSED

    @property
    def can_retry(self) -> bool:
        return self.state in (DownloadState.FAILED, DownloadState.CANCELLED)

    @property
    def can_cancel(self) -> bool:
        return self.state in (DownloadState.QUEUED, DownloadState.RUNNING, DownloadState.PAUSED) and self.cancellable

    def is_same_download(self, request: DownloadRequest) -> bool:
        return self.request == request
