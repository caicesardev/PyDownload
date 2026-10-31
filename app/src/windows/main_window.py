import shutil
from datetime import datetime
from typing import Any

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QMessageBox, QStackedWidget, QWidget

from constants import APP_NAME, VERSION
from src.browser.secure_profile import SecureProfile
from src.models.download_job import DownloadJob
from src.models.download_request import DownloadRequest
from src.models.history_entry import HistoryEntry
from src.models.video_metadata import VideoMetadata
from src.pages.about_page import AboutPage
from src.pages.browser_page import BrowserPage
from src.pages.downloads_page import DownloadsPage
from src.pages.history_page import HistoryPage
from src.pages.settings_page import SettingsPage
from src.services.download_queue import DownloadQueue
from src.services.ffmpeg_locator import locate_ffmpeg
from src.services.history_store import HistoryStore
from src.services.metadata_service import MetadataService
from src.services.thumbnail_loader import ThumbnailLoader
from src.services.ydl_options import base_options
from src.settings.app_paths import history_file, partial_downloads_directory
from src.settings.preferences import Preferences
from src.widgets.icons import app_icon
from src.widgets.sidebar import Sidebar, SidebarEntry
from src.workers.download_worker import DownloadWorker

STATUS_MESSAGE_MILLISECONDS = 5000
DEFAULT_WINDOW_SIZE = (1360, 860)
BROWSER_PAGE, DOWNLOADS_PAGE, HISTORY_PAGE, SETTINGS_PAGE, ABOUT_PAGE = range(5)
SIDEBAR_ENTRIES = [
    SidebarEntry("Navegador", "globe"),
    SidebarEntry("Descargas", "download"),
    SidebarEntry("Historial", "history"),
    SidebarEntry("Ajustes", "settings"),
    SidebarEntry("Acerca de", "info"),
]


class MainWindow(QMainWindow):
    def __init__(self, profile: SecureProfile) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {VERSION}")
        self.setWindowIcon(app_icon())
        self._preferences = Preferences()
        self._profile = profile
        self._was_maximized_before_full_screen = False
        self._thumbnail_loader = ThumbnailLoader(self)
        self._metadata_service = MetadataService(self._ydl_options, self)
        self._discard_stale_partial_downloads()
        self._queue = DownloadQueue(
            self._create_download_worker,
            partial_downloads_directory(),
            self._preferences.max_concurrent_downloads,
        )
        self._queue.setParent(self)

        self._sidebar = Sidebar(SIDEBAR_ENTRIES, self)
        self._browser_page = BrowserPage(profile, self._metadata_service, self._thumbnail_loader, self._preferences, self)
        self._downloads_page = DownloadsPage(self._queue, self._thumbnail_loader, self._preferences, self)
        self._history_page = HistoryPage(HistoryStore(history_file()), self)
        self._settings_page = SettingsPage(self._preferences, self)
        self._pages = QStackedWidget(self)
        for page in (self._browser_page, self._downloads_page, self._history_page, self._settings_page, AboutPage(self)):
            self._pages.addWidget(page)

        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._sidebar)
        layout.addWidget(self._pages, stretch=1)
        self.setCentralWidget(central)

        self._connect_signals()
        self._restore_geometry()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._queue.pending_count and not self._confirm_exit_with_pending_downloads():
            event.ignore()
            return
        self._preferences.window_geometry = self.saveGeometry()
        self.hide()
        self._queue.shutdown()
        self._metadata_service.wait_for_workers()
        self._browser_page.release_page()
        event.accept()

    def _connect_signals(self) -> None:
        self._sidebar.page_selected.connect(self._show_page)
        self._browser_page.download_requested.connect(self._enqueue_download)
        self._browser_page.status_message.connect(self._show_status)
        self._browser_page.full_screen_changed.connect(self._set_browser_full_screen)
        self._queue.pending_count_changed.connect(lambda count: self._sidebar.set_badge(DOWNLOADS_PAGE, count))
        self._queue.job_completed.connect(self._record_completed_download)
        self._settings_page.settings_saved.connect(self._apply_settings)
        self._settings_page.clear_browsing_data_requested.connect(self._profile.clear_browsing_data)

    def _show_page(self, index: int) -> None:
        if index == SETTINGS_PAGE:
            self._settings_page.load()
        self._pages.setCurrentIndex(index)

    def _ydl_options(self) -> dict[str, Any]:
        ffmpeg_location = locate_ffmpeg(self._preferences.ffmpeg_location)
        return base_options(ffmpeg_location, self._preferences.rate_limit_kib)

    def _create_download_worker(self, job: DownloadJob) -> DownloadWorker:
        return DownloadWorker(job.job_id, job.request, self._ydl_options(), job.temp_directory)

    def _enqueue_download(self, request: DownloadRequest, metadata: VideoMetadata) -> None:
        if request.requires_ffmpeg and locate_ffmpeg(self._preferences.ffmpeg_location) is None:
            QMessageBox.warning(
                self,
                "FFmpeg no disponible",
                "Este formato necesita FFmpeg. Indica su ubicación en Ajustes o elige un formato que ya incluya audio.",
            )
            return
        if self._queue.find_pending(request) is not None:
            self._show_status(f"«{metadata.title}» ya está en la cola con ese formato.")
            return
        self._queue.enqueue(request, metadata.title, metadata.thumbnail_url)
        self._show_status(f"Añadido a la cola: {metadata.title}")

    def _record_completed_download(self, job: DownloadJob) -> None:
        self._history_page.add_entry(HistoryEntry(
            title=job.title,
            url=job.request.url,
            summary=job.request.summary,
            filepath=job.filepath,
            completed_at=datetime.now().isoformat(timespec="seconds"),
        ))
        self._show_status(f"Descarga completada: {job.title}")

    def _apply_settings(self) -> None:
        self._queue.set_max_concurrent(self._preferences.max_concurrent_downloads)

    def _set_browser_full_screen(self, is_full_screen: bool) -> None:
        self._sidebar.setVisible(not is_full_screen)
        self.statusBar().setVisible(not is_full_screen)
        if is_full_screen:
            self._was_maximized_before_full_screen = self.isMaximized()
            self.showFullScreen()
        elif self._was_maximized_before_full_screen:
            self.showMaximized()
        else:
            self.showNormal()

    def _show_status(self, message: str) -> None:
        self.statusBar().showMessage(message, STATUS_MESSAGE_MILLISECONDS)

    def _confirm_exit_with_pending_downloads(self) -> bool:
        answer = QMessageBox.question(
            self,
            "Descargas pendientes",
            f"Hay {self._queue.pending_count} descargas sin terminar. Si sales se detendrán "
            "y los archivos parciales se descartarán. ¿Salir de todas formas?",
        )
        return answer == QMessageBox.StandardButton.Yes

    def _restore_geometry(self) -> None:
        geometry = self._preferences.window_geometry
        if geometry is None or not self.restoreGeometry(geometry):
            self.resize(*DEFAULT_WINDOW_SIZE)

    @staticmethod
    def _discard_stale_partial_downloads() -> None:
        shutil.rmtree(partial_downloads_directory(), ignore_errors=True)
