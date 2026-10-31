import itertools
import shutil
import uuid
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from src.models.download_job import DownloadJob, DownloadState
from src.models.download_request import DownloadRequest
from src.workers.download_worker import DownloadWorker

WorkerFactory = Callable[[DownloadJob], DownloadWorker]
SHUTDOWN_WAIT_MILLISECONDS = 10_000


class DownloadQueue(QObject):
    job_added = Signal(object)
    job_changed = Signal(object)
    job_removed = Signal(int)
    job_completed = Signal(object)
    pending_count_changed = Signal(int)

    def __init__(self, worker_factory: WorkerFactory, temp_root: Path, max_concurrent: int) -> None:
        super().__init__()
        self._worker_factory = worker_factory
        self._temp_root = temp_root
        self._max_concurrent = max_concurrent
        self._jobs: dict[int, DownloadJob] = {}
        self._workers: dict[int, DownloadWorker] = {}
        self._job_ids = itertools.count(1)

    @property
    def jobs(self) -> tuple[DownloadJob, ...]:
        return tuple(self._jobs.values())

    @property
    def pending_count(self) -> int:
        return sum(job.is_pending for job in self._jobs.values())

    @property
    def has_running_workers(self) -> bool:
        return bool(self._workers)

    def job(self, job_id: int) -> DownloadJob | None:
        return self._jobs.get(job_id)

    def find_pending(self, request: DownloadRequest) -> DownloadJob | None:
        return next((job for job in self._jobs.values() if job.is_pending and job.is_same_download(request)), None)

    def enqueue(self, request: DownloadRequest, title: str, thumbnail_url: str) -> DownloadJob:
        job = DownloadJob(
            job_id=next(self._job_ids),
            request=request,
            title=title,
            thumbnail_url=thumbnail_url,
            temp_directory=self._temp_root / uuid.uuid4().hex,
        )
        self._jobs[job.job_id] = job
        self.job_added.emit(job)
        self._schedule()
        self._notify_pending_count()
        return job

    def set_max_concurrent(self, max_concurrent: int) -> None:
        self._max_concurrent = max_concurrent
        self._schedule()

    def pause(self, job_id: int) -> None:
        job = self._jobs[job_id]
        if not job.can_pause:
            return
        if job.state is DownloadState.QUEUED:
            self._update(job, state=DownloadState.PAUSED, detail="")
            return
        self._update(job, state=DownloadState.PAUSING)
        self._workers[job_id].request_pause()

    def resume(self, job_id: int) -> None:
        job = self._jobs[job_id]
        if job.can_resume or job.can_retry:
            if job.state is DownloadState.CANCELLED:
                job.progress = 0.0
            self._update(job, state=DownloadState.QUEUED, detail="", error="", cancellable=True)
            self._schedule()

    def cancel(self, job_id: int) -> None:
        job = self._jobs[job_id]
        if not job.can_cancel:
            return
        if job.state is DownloadState.RUNNING:
            self._update(job, state=DownloadState.CANCELLING)
            self._workers[job_id].request_cancel()
            return
        self._discard_partial_files(job)
        self._update(job, state=DownloadState.CANCELLED, progress=0.0, detail="")

    def remove(self, job_id: int) -> None:
        job = self._jobs[job_id]
        if not job.is_finished:
            return
        self._discard_partial_files(job)
        del self._jobs[job_id]
        self.job_removed.emit(job_id)

    def pause_all(self) -> None:
        for job in self.jobs:
            self.pause(job.job_id)

    def resume_all(self) -> None:
        for job in self.jobs:
            if job.can_resume:
                self.resume(job.job_id)

    def clear_finished(self) -> None:
        for job in self.jobs:
            if job.state in (DownloadState.COMPLETED, DownloadState.CANCELLED):
                self.remove(job.job_id)

    def shutdown(self) -> None:
        self._max_concurrent = 0
        workers = list(self._workers.values())
        for worker in workers:
            worker.request_pause()
        for worker in workers:
            if not worker.wait(SHUTDOWN_WAIT_MILLISECONDS):
                worker.terminate()
                worker.wait()

    def _schedule(self) -> None:
        for job in self._jobs.values():
            if len(self._workers) >= self._max_concurrent:
                return
            if job.state is DownloadState.QUEUED and job.job_id not in self._workers:
                self._start(job)

    def _start(self, job: DownloadJob) -> None:
        worker = self._worker_factory(job)
        worker.progress_changed.connect(self._on_progress)
        worker.phase_changed.connect(self._on_phase_changed)
        worker.completed.connect(self._on_completed)
        worker.failed.connect(self._on_failed)
        worker.paused.connect(self._on_paused)
        worker.cancelled.connect(self._on_cancelled)
        worker.finished.connect(self._on_worker_finished)
        self._workers[job.job_id] = worker
        self._update(job, state=DownloadState.RUNNING, detail="Preparando descarga…", cancellable=True)
        worker.start()

    def _on_progress(self, job_id: int, percent: float, detail: str) -> None:
        job = self._jobs.get(job_id)
        if job and job.state is DownloadState.RUNNING:
            self._update(job, progress=percent, detail=detail)

    def _on_phase_changed(self, job_id: int, detail: str, cancellable: bool) -> None:
        if job := self._jobs.get(job_id):
            self._update(job, detail=detail, cancellable=cancellable)

    def _on_completed(self, job_id: int, filepath: str) -> None:
        if job := self._jobs.get(job_id):
            self._update(job, state=DownloadState.COMPLETED, progress=100.0, filepath=filepath, detail=Path(filepath).name)
            self.job_completed.emit(job)

    def _on_failed(self, job_id: int, message: str) -> None:
        job = self._jobs.get(job_id)
        if job is None:
            return
        if job.state is DownloadState.CANCELLING:
            self._on_cancelled(job_id)
            return
        self._update(job, state=DownloadState.FAILED, error=message, detail=message, cancellable=True)

    def _on_paused(self, job_id: int) -> None:
        if job := self._jobs.get(job_id):
            self._update(job, state=DownloadState.PAUSED, detail="")

    def _on_cancelled(self, job_id: int) -> None:
        if job := self._jobs.get(job_id):
            self._discard_partial_files(job)
            self._update(job, state=DownloadState.CANCELLED, progress=0.0, detail="", cancellable=True)

    def _on_worker_finished(self) -> None:
        worker = self.sender()
        if not isinstance(worker, DownloadWorker):
            return
        self._workers.pop(worker.job_id, None)
        worker.wait()
        worker.deleteLater()
        self._schedule()

    def _update(self, job: DownloadJob, **changes: object) -> None:
        for name, value in changes.items():
            setattr(job, name, value)
        self.job_changed.emit(job)
        if "state" in changes:
            self._notify_pending_count()

    def _notify_pending_count(self) -> None:
        self.pending_count_changed.emit(self.pending_count)

    @staticmethod
    def _discard_partial_files(job: DownloadJob) -> None:
        shutil.rmtree(job.temp_directory, ignore_errors=True)
