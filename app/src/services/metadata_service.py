from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Signal

from src.models.video_metadata import VideoMetadata
from src.services.youtube_url import canonical_watch_url
from src.workers.metadata_worker import MetadataWorker

OptionsProvider = Callable[[], dict[str, Any]]


class MetadataService(QObject):
    loading = Signal(str)
    metadata_ready = Signal(object)
    failed = Signal(str, str)

    def __init__(self, options_provider: OptionsProvider, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._options_provider = options_provider
        self._cache: dict[str, VideoMetadata] = {}
        self._workers: set[MetadataWorker] = set()
        self._requested_video_id: str | None = None

    def request(self, video_id: str) -> None:
        self._requested_video_id = video_id
        if cached := self._cache.get(video_id):
            self.metadata_ready.emit(cached)
            return
        self.loading.emit(video_id)
        worker = MetadataWorker(video_id, canonical_watch_url(video_id), self._options_provider())
        worker.metadata_ready.connect(self._on_metadata_ready)
        worker.failed.connect(self._on_failed)
        worker.finished.connect(self._on_worker_finished)
        self._workers.add(worker)
        worker.start()

    def forget_request(self) -> None:
        self._requested_video_id = None

    def wait_for_workers(self) -> None:
        for worker in list(self._workers):
            worker.wait()

    def _on_metadata_ready(self, video_id: str, metadata: VideoMetadata) -> None:
        self._cache[video_id] = metadata
        if video_id == self._requested_video_id:
            self.metadata_ready.emit(metadata)

    def _on_failed(self, video_id: str, message: str) -> None:
        if video_id == self._requested_video_id:
            self.failed.emit(video_id, message)

    def _on_worker_finished(self) -> None:
        worker = self.sender()
        if isinstance(worker, MetadataWorker):
            self._workers.discard(worker)
            worker.deleteLater()
