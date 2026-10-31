from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.models.download_job import DownloadJob, DownloadState
from src.services.download_queue import DownloadQueue
from src.services.thumbnail_loader import ThumbnailLoader
from src.settings.preferences import Preferences
from src.utils.file_browser import open_directory, reveal_in_file_manager
from src.widgets.buttons import icon_button
from src.widgets.download_item import DownloadAction, DownloadItem
from src.widgets.empty_state import EmptyState
from src.widgets.icons import themed_icon
from src.widgets.labels import muted_label, page_title


class DownloadsPage(QWidget):
    def __init__(
        self,
        queue: DownloadQueue,
        thumbnail_loader: ThumbnailLoader,
        preferences: Preferences,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("Page")
        self._queue = queue
        self._thumbnail_loader = thumbnail_loader
        self._preferences = preferences
        self._items: dict[int, DownloadItem] = {}

        self._summary = muted_label(parent=self)
        self._stack = QStackedWidget(self)
        self._empty_state = EmptyState(
            "inbox",
            "No hay descargas en la cola",
            "Abre un vídeo en el navegador, elige el formato en el panel lateral y pulsa «Añadir a la cola».",
            self,
        )
        self._stack.addWidget(self._empty_state)
        self._stack.addWidget(self._build_list())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.addLayout(self._build_header())
        layout.addWidget(self._summary)
        layout.addWidget(self._stack, stretch=1)

        self._connect_queue()
        self._refresh_summary()

    def _build_header(self) -> QHBoxLayout:
        pause_all = icon_button(themed_icon("pause"), "Pausar todo", self)
        pause_all.clicked.connect(self._queue.pause_all)
        resume_all = icon_button(themed_icon("play"), "Reanudar todo", self)
        resume_all.clicked.connect(self._queue.resume_all)
        clear_finished = icon_button(themed_icon("list-x"), "Limpiar finalizadas", self)
        clear_finished.clicked.connect(self._queue.clear_finished)
        open_folder = icon_button(themed_icon("folder-open"), "Abrir carpeta de descargas", self)
        open_folder.clicked.connect(self._open_download_directory)

        header = QHBoxLayout()
        header.addWidget(page_title("Descargas", self))
        header.addStretch()
        for button in (pause_all, resume_all, clear_finished, open_folder):
            header.addWidget(button)
        return header

    def _build_list(self) -> QScrollArea:
        container = QWidget(self)
        self._list_layout = QVBoxLayout(container)
        self._list_layout.setContentsMargins(0, 0, 4, 0)
        self._list_layout.setSpacing(10)
        self._list_layout.addStretch()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(container)
        return scroll_area

    def _connect_queue(self) -> None:
        self._queue.job_added.connect(self._add_item)
        self._queue.job_changed.connect(self._update_item)
        self._queue.job_removed.connect(self._remove_item)
        self._thumbnail_loader.thumbnail_ready.connect(self._apply_thumbnail)

    def _add_item(self, job: DownloadJob) -> None:
        item = DownloadItem(job, self)
        item.action_requested.connect(self._handle_action)
        self._items[job.job_id] = item
        self._list_layout.insertWidget(self._list_layout.count() - 1, item)
        self._thumbnail_loader.load(job.thumbnail_url)
        self._refresh_summary()

    def _update_item(self, job: DownloadJob) -> None:
        if item := self._items.get(job.job_id):
            item.update_from(job)
        self._refresh_summary()

    def _remove_item(self, job_id: int) -> None:
        if item := self._items.pop(job_id, None):
            item.deleteLater()
        self._refresh_summary()

    def _apply_thumbnail(self, url: str, pixmap: QPixmap) -> None:
        for job in self._queue.jobs:
            if job.thumbnail_url == url and job.job_id in self._items:
                self._items[job.job_id].set_thumbnail(pixmap)

    def _handle_action(self, job_id: int, action: DownloadAction) -> None:
        match action:
            case DownloadAction.PAUSE:
                self._queue.pause(job_id)
            case DownloadAction.RESUME | DownloadAction.RETRY:
                self._queue.resume(job_id)
            case DownloadAction.CANCEL:
                self._confirm_cancel(job_id)
            case DownloadAction.OPEN_FOLDER:
                self._reveal_job_file(job_id)
            case DownloadAction.REMOVE:
                self._queue.remove(job_id)

    def _confirm_cancel(self, job_id: int) -> None:
        answer = QMessageBox.question(
            self,
            "Cancelar descarga",
            "¿Cancelar la descarga? Se borrarán los archivos parciales.",
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._queue.cancel(job_id)

    def _reveal_job_file(self, job_id: int) -> None:
        job = self._queue.job(job_id)
        if job is None or not reveal_in_file_manager(job.filepath or str(job.request.destination)):
            QMessageBox.warning(self, "Archivo no encontrado", "El archivo ya no existe en la carpeta de descargas.")

    def _open_download_directory(self) -> None:
        directory = self._preferences.download_directory
        if not open_directory(directory):
            QMessageBox.warning(self, "Carpeta no encontrada", f"La carpeta {directory} no existe todavía.")

    def _refresh_summary(self) -> None:
        jobs = self._queue.jobs
        self._stack.setCurrentIndex(1 if jobs else 0)
        running = sum(job.is_active for job in jobs)
        queued = sum(job.state is DownloadState.QUEUED for job in jobs)
        paused = sum(job.state is DownloadState.PAUSED for job in jobs)
        completed = sum(job.state is DownloadState.COMPLETED for job in jobs)
        failed = sum(job.state is DownloadState.FAILED for job in jobs)
        self._summary.setText(
            f"{running} en curso · {queued} en cola · {paused} en pausa · {completed} completadas · {failed} con error"
            f" — máximo {self._preferences.max_concurrent_downloads} simultáneas"
        )
