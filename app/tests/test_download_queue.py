import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import QCoreApplication

from src.models.download_job import DownloadJob, DownloadState
from src.models.download_request import AudioDownloadRequest, AudioOutput
from src.models.media_format import AudioFormat
from src.services.download_queue import DownloadQueue
from src.workers.download_worker import DownloadWorker

APPLICATION = QCoreApplication.instance() or QCoreApplication([])
OPUS_AUDIO = AudioFormat("251", "webm", "opus", 126, None, None)


class FakeWorker(DownloadWorker):
    def __init__(self, job: DownloadJob) -> None:
        super().__init__(job.job_id, job.request, {}, job.temp_directory)
        self.started = False
        self.pause_requested = False
        self.cancel_requested = False

    def start(self, *_args: object) -> None:
        self.started = True

    def wait(self, *_args: object) -> bool:
        return True

    def request_pause(self) -> None:
        self.pause_requested = True

    def request_cancel(self) -> None:
        self.cancel_requested = True

    def finish(self) -> None:
        self.finished.emit()


class DownloadQueueTest(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.temp_root = Path(self._temp.name)
        self.workers: dict[int, FakeWorker] = {}
        self.queue = DownloadQueue(self._create_worker, self.temp_root, max_concurrent=2)
        self.pending_counts: list[int] = []
        self.completed: list[DownloadJob] = []
        self.queue.pending_count_changed.connect(self.pending_counts.append)
        self.queue.job_completed.connect(self.completed.append)

    def tearDown(self) -> None:
        self._temp.cleanup()

    def _create_worker(self, job: DownloadJob) -> FakeWorker:
        worker = FakeWorker(job)
        self.workers[job.job_id] = worker
        return worker

    def _enqueue(self, video_id: str) -> DownloadJob:
        request = AudioDownloadRequest(
            f"https://www.youtube.com/watch?v={video_id}", self.temp_root / "out", OPUS_AUDIO, AudioOutput.MP3,
        )
        return self.queue.enqueue(request, video_id, "")

    def test_respects_the_concurrency_limit(self) -> None:
        jobs = [self._enqueue(f"video{index:06}") for index in range(3)]
        self.assertEqual([job.state for job in jobs], [DownloadState.RUNNING, DownloadState.RUNNING, DownloadState.QUEUED])
        self.assertEqual(sorted(self.workers), [jobs[0].job_id, jobs[1].job_id])

    def test_starts_the_next_job_when_a_worker_finishes(self) -> None:
        first, _second, third = [self._enqueue(f"video{index:06}") for index in range(3)]
        self.workers[first.job_id].completed.emit(first.job_id, "C:/out/video.mp3")
        self.workers[first.job_id].finish()
        self.assertIs(first.state, DownloadState.COMPLETED)
        self.assertIs(third.state, DownloadState.RUNNING)
        self.assertEqual(self.completed, [first])

    def test_raising_the_limit_starts_queued_jobs(self) -> None:
        jobs = [self._enqueue(f"video{index:06}") for index in range(3)]
        self.queue.set_max_concurrent(3)
        self.assertIs(jobs[2].state, DownloadState.RUNNING)

    def test_pausing_a_running_job_waits_for_the_worker(self) -> None:
        job = self._enqueue("video000001")
        self.queue.pause(job.job_id)
        self.assertIs(job.state, DownloadState.PAUSING)
        self.assertTrue(self.workers[job.job_id].pause_requested)
        self.workers[job.job_id].paused.emit(job.job_id)
        self.assertIs(job.state, DownloadState.PAUSED)

    def test_pausing_a_queued_job_never_starts_it(self) -> None:
        self.queue.set_max_concurrent(0)
        job = self._enqueue("video000001")
        self.queue.pause(job.job_id)
        self.queue.set_max_concurrent(1)
        self.assertIs(job.state, DownloadState.PAUSED)
        self.assertNotIn(job.job_id, self.workers)

    def test_resuming_requeues_and_restarts(self) -> None:
        job = self._enqueue("video000001")
        worker = self.workers[job.job_id]
        self.queue.pause(job.job_id)
        worker.paused.emit(job.job_id)
        worker.finish()
        self.queue.resume(job.job_id)
        self.assertIs(job.state, DownloadState.RUNNING)
        self.assertIsNot(self.workers[job.job_id], worker)

    def test_cancelling_a_paused_job_discards_partial_files(self) -> None:
        job = self._enqueue("video000001")
        job.temp_directory.mkdir(parents=True)
        (job.temp_directory / "video.webm.part").write_bytes(b"partial")
        self.queue.pause(job.job_id)
        self.workers[job.job_id].paused.emit(job.job_id)
        self.queue.cancel(job.job_id)
        self.assertIs(job.state, DownloadState.CANCELLED)
        self.assertFalse(job.temp_directory.exists())

    def test_cancelling_a_running_job_is_delegated_to_the_worker(self) -> None:
        job = self._enqueue("video000001")
        self.queue.cancel(job.job_id)
        self.assertIs(job.state, DownloadState.CANCELLING)
        self.assertTrue(self.workers[job.job_id].cancel_requested)
        self.workers[job.job_id].failed.emit(job.job_id, "interrupted")
        self.assertIs(job.state, DownloadState.CANCELLED)

    def test_failed_jobs_can_be_retried(self) -> None:
        job = self._enqueue("video000001")
        worker = self.workers[job.job_id]
        worker.failed.emit(job.job_id, "HTTP Error 403")
        worker.finish()
        self.assertIs(job.state, DownloadState.FAILED)
        self.assertEqual(job.error, "HTTP Error 403")
        self.queue.resume(job.job_id)
        self.assertIs(job.state, DownloadState.RUNNING)
        self.assertEqual(job.error, "")

    def test_postprocessing_jobs_cannot_be_interrupted(self) -> None:
        job = self._enqueue("video000001")
        self.workers[job.job_id].phase_changed.emit(job.job_id, "Uniendo vídeo y audio…", False)
        self.queue.pause(job.job_id)
        self.queue.cancel(job.job_id)
        self.assertIs(job.state, DownloadState.RUNNING)

    def test_finds_duplicate_pending_requests(self) -> None:
        job = self._enqueue("video000001")
        self.assertIs(self.queue.find_pending(job.request), job)
        self.workers[job.job_id].completed.emit(job.job_id, "C:/out/video.mp3")
        self.assertIsNone(self.queue.find_pending(job.request))

    def test_only_finished_jobs_can_be_removed(self) -> None:
        running = self._enqueue("video000001")
        self.queue.remove(running.job_id)
        self.assertIn(running, self.queue.jobs)
        self.workers[running.job_id].completed.emit(running.job_id, "C:/out/video.mp3")
        self.queue.clear_finished()
        self.assertEqual(self.queue.jobs, ())

    def test_reports_pending_counts(self) -> None:
        job = self._enqueue("video000001")
        self.workers[job.job_id].completed.emit(job.job_id, "C:/out/video.mp3")
        self.assertEqual(self.pending_counts[-1], 0)
        self.assertIn(1, self.pending_counts)


if __name__ == "__main__":
    unittest.main()
