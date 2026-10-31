from collections.abc import Callable
from urllib.parse import urlsplit

from PySide6.QtCore import QSize, Qt, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QIcon, QKeySequence, QPixmap, QShortcut
from PySide6.QtWebEngineCore import QWebEngineFullScreenRequest, QWebEnginePage, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from constants import YOUTUBE_HOME_URL
from src.browser.secure_page import SecurePage
from src.models.video_metadata import VideoMetadata
from src.services.metadata_service import MetadataService
from src.services.thumbnail_loader import ThumbnailLoader
from src.services.youtube_url import extract_video_id, search_url, thumbnail_url
from src.settings.preferences import Preferences
from src.widgets.video_panel import VideoPanel

VIDEO_DETECTION_DELAY_MILLISECONDS = 400
NAVIGATION_ICON_SIZE = QSize(20, 20)


class BrowserPage(QWidget):
    download_requested = Signal(object, object)
    status_message = Signal(str)
    full_screen_changed = Signal(bool)

    def __init__(
        self,
        profile: QWebEngineProfile,
        metadata_service: MetadataService,
        thumbnail_loader: ThumbnailLoader,
        preferences: Preferences,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("Page")
        self._metadata_service = metadata_service
        self._thumbnail_loader = thumbnail_loader
        self._detected_video_id: str | None = None

        self._view = QWebEngineView(self)
        self._page = SecurePage(profile, self._view)
        self._view.setPage(self._page)
        self._panel = VideoPanel(preferences, self)
        self._toolbar = self._build_toolbar()

        self._detection_timer = QTimer(self)
        self._detection_timer.setSingleShot(True)
        self._detection_timer.setInterval(VIDEO_DETECTION_DELAY_MILLISECONDS)
        self._detection_timer.timeout.connect(self._request_detected_metadata)

        self._connect_signals()
        self._build_layout()
        self.go_home()

    def go_home(self) -> None:
        self._view.setUrl(QUrl(YOUTUBE_HOME_URL))

    def release_page(self) -> None:
        self._view.setPage(None)
        self._page.deleteLater()

    def _build_toolbar(self) -> QFrame:
        toolbar = QFrame(self)
        toolbar.setObjectName("Toolbar")
        self._back_button = self._navigation_button(self._standard_icon(QStyle.StandardPixmap.SP_ArrowBack), "Atrás", self._view.back)
        self._forward_button = self._navigation_button(self._standard_icon(QStyle.StandardPixmap.SP_ArrowForward), "Adelante", self._view.forward)
        reload_button = self._navigation_button(self._standard_icon(QStyle.StandardPixmap.SP_BrowserReload), "Recargar", self._view.reload)
        home_button = self._navigation_button(QIcon(":/icons/home.png"), "Inicio de YouTube", self.go_home)

        self._address_bar = QLineEdit(toolbar)
        self._address_bar.setObjectName("AddressBar")
        self._address_bar.setPlaceholderText("Busca en YouTube o pega el enlace de un vídeo")
        self._address_bar.setClearButtonEnabled(True)
        self._address_bar.returnPressed.connect(self._navigate_from_address_bar)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)
        for button in (self._back_button, self._forward_button, reload_button, home_button):
            layout.addWidget(button)
        layout.addWidget(self._address_bar, stretch=1)
        return toolbar

    def _standard_icon(self, pixmap: QStyle.StandardPixmap) -> QIcon:
        return self.style().standardIcon(pixmap)

    def _navigation_button(self, icon: QIcon, tooltip: str, action: Callable[[], None]) -> QToolButton:
        button = QToolButton(self)
        button.setObjectName("NavigationButton")
        button.setIcon(icon)
        button.setIconSize(NAVIGATION_ICON_SIZE)
        button.setToolTip(tooltip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(action)
        return button

    def _build_layout(self) -> None:
        browser_column = QVBoxLayout()
        browser_column.setSpacing(8)
        browser_column.addWidget(self._toolbar)
        browser_column.addWidget(self._view, stretch=1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        layout.addLayout(browser_column, stretch=1)
        layout.addWidget(self._panel)
        self._content_layout = layout

    def _connect_signals(self) -> None:
        self._view.urlChanged.connect(self._on_url_changed)
        self._page.external_link_requested.connect(self._confirm_external_link)
        self._page.navigation_blocked.connect(self._report_blocked_navigation)
        self._page.fullScreenRequested.connect(self._on_full_screen_requested)
        self._panel.download_requested.connect(self.download_requested)
        self._panel.retry_requested.connect(self._request_detected_metadata)
        self._metadata_service.loading.connect(self._on_metadata_loading)
        self._metadata_service.metadata_ready.connect(self._on_metadata_ready)
        self._metadata_service.failed.connect(self._on_metadata_failed)
        self._thumbnail_loader.thumbnail_ready.connect(self._on_thumbnail_ready)
        exit_full_screen = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        exit_full_screen.activated.connect(lambda: self._page.triggerAction(QWebEnginePage.WebAction.ExitFullScreen))

    def _on_url_changed(self, url: QUrl) -> None:
        self._address_bar.setText(url.toString())
        self._address_bar.setCursorPosition(0)
        self._back_button.setEnabled(self._view.history().canGoBack())
        self._forward_button.setEnabled(self._view.history().canGoForward())
        video_id = extract_video_id(url.toString())
        if video_id == self._detected_video_id:
            return
        self._detected_video_id = video_id
        if video_id is None:
            self._detection_timer.stop()
            self._metadata_service.forget_request()
            self._panel.show_idle()
            return
        self._panel.clear_thumbnail()
        self._panel.show_loading()
        self._thumbnail_loader.load(thumbnail_url(video_id))
        self._detection_timer.start()

    def _request_detected_metadata(self) -> None:
        if self._detected_video_id is not None:
            self._metadata_service.request(self._detected_video_id)

    def _on_metadata_loading(self, video_id: str) -> None:
        if video_id == self._detected_video_id:
            self._panel.show_loading()

    def _on_metadata_ready(self, metadata: VideoMetadata) -> None:
        if metadata.video_id == self._detected_video_id:
            self._panel.show_metadata(metadata)
            self._thumbnail_loader.load(metadata.thumbnail_url)

    def _on_metadata_failed(self, video_id: str, message: str) -> None:
        if video_id == self._detected_video_id:
            self._panel.show_error(message)

    def _on_thumbnail_ready(self, url: str, pixmap: QPixmap) -> None:
        if self._detected_video_id is not None and url == thumbnail_url(self._detected_video_id):
            self._panel.set_thumbnail(pixmap)

    def _navigate_from_address_bar(self) -> None:
        text = self._address_bar.text().strip()
        if not text:
            return
        target = text if self._looks_like_url(text) else search_url(text)
        self._view.setUrl(QUrl.fromUserInput(target))
        self._view.setFocus()

    @staticmethod
    def _looks_like_url(text: str) -> bool:
        if " " in text:
            return False
        candidate = text if "://" in text else f"https://{text}"
        host = urlsplit(candidate).hostname or ""
        return "." in host

    def _confirm_external_link(self, url: QUrl) -> None:
        answer = QMessageBox.question(
            self,
            "Abrir enlace externo",
            f"Este enlace sale de YouTube:\n\n{url.toString()}\n\n¿Quieres abrirlo en tu navegador predeterminado?",
        )
        if answer == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(url)

    def _report_blocked_navigation(self, url: QUrl) -> None:
        self.status_message.emit(f"Navegación bloqueada por seguridad: {url.host() or url.scheme()}")

    def _on_full_screen_requested(self, request: QWebEngineFullScreenRequest) -> None:
        request.accept()
        is_full_screen = request.toggleOn()
        self._toolbar.setVisible(not is_full_screen)
        self._panel.setVisible(not is_full_screen)
        margin = 0 if is_full_screen else 12
        self._content_layout.setContentsMargins(margin, margin, margin, margin)
        self.full_screen_changed.emit(is_full_screen)
