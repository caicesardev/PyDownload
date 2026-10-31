from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.models.download_request import (
    AudioDownloadRequest,
    AudioOutput,
    DownloadRequest,
    MediaKind,
    VideoDownloadRequest,
)
from src.models.media_format import AudioFormat, VideoFormat
from src.models.video_metadata import VideoMetadata
from src.settings.preferences import Preferences
from src.widgets.buttons import icon_button
from src.widgets.empty_state import EmptyState
from src.widgets.icons import themed_icon
from src.widgets.labels import muted_label, section_title, show_scaled_pixmap, thumbnail_label
from src.widgets.theme import ACCENT, MUTED_TEXT, ON_ACCENT, set_style_property

PANEL_WIDTH = 360
THUMBNAIL_WIDTH = 320
THUMBNAIL_HEIGHT = 180


class VideoPanel(QFrame):
    download_requested = Signal(object, object)
    retry_requested = Signal()

    def __init__(self, preferences: Preferences, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("VideoPanel")
        self.setFixedWidth(PANEL_WIDTH)
        self._preferences = preferences
        self._metadata: VideoMetadata | None = None

        self._stack = QStackedWidget(self)
        self._idle_page = EmptyState(
            "monitor-play",
            "Ningún vídeo seleccionado",
            "Abre un vídeo de YouTube en el navegador y aquí verás sus formatos de vídeo y audio disponibles.",
            self,
        )
        self._stack.addWidget(self._idle_page)
        self._stack.addWidget(self._build_content_page())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)
        self.show_idle()

    def show_idle(self) -> None:
        self._metadata = None
        self._stack.setCurrentWidget(self._idle_page)

    def show_loading(self) -> None:
        self._metadata = None
        self._stack.setCurrentWidget(self._content_page)
        self._title.setText("Cargando información del vídeo…")
        self._details.setText("")
        self._set_status("Obteniendo formatos disponibles…", "")
        self._set_form_enabled(False)
        self._retry_button.hide()

    def show_metadata(self, metadata: VideoMetadata) -> None:
        self._metadata = metadata
        self._stack.setCurrentWidget(self._content_page)
        self._title.setText(metadata.title)
        self._details.setText(metadata.details)
        self._retry_button.hide()
        if not metadata.has_formats:
            self._set_status("Este vídeo no tiene formatos descargables.", "error")
            self._set_form_enabled(False)
            return
        self._video_button.setEnabled(bool(metadata.video_formats))
        self._audio_button.setEnabled(bool(metadata.audio_formats))
        self._select_initial_kind(metadata)
        self._set_form_enabled(True)
        self._set_status("", "")

    def show_error(self, message: str) -> None:
        self._metadata = None
        self._stack.setCurrentWidget(self._content_page)
        self._title.setText("No se pudo obtener la información del vídeo")
        self._details.setText("")
        self._set_status(message, "error")
        self._set_form_enabled(False)
        self._retry_button.show()

    def set_thumbnail(self, pixmap: QPixmap) -> None:
        show_scaled_pixmap(self._thumbnail, pixmap)

    def clear_thumbnail(self) -> None:
        self._thumbnail.clear()

    def _build_content_page(self) -> QWidget:
        self._content_page = QWidget(self)
        self._thumbnail = thumbnail_label(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, self._content_page)

        self._title = QLabel(self._content_page)
        self._title.setObjectName("ItemTitle")
        self._title.setWordWrap(True)
        self._details = muted_label(parent=self._content_page)

        self._video_button = self._segment_button("Vídeo", "video")
        self._audio_button = self._segment_button("Audio", "music")
        self._kind_group = QButtonGroup(self)
        self._kind_group.addButton(self._video_button)
        self._kind_group.addButton(self._audio_button)
        self._kind_group.buttonToggled.connect(self._on_kind_toggled)
        segments = QHBoxLayout()
        segments.setSpacing(6)
        segments.addWidget(self._video_button)
        segments.addWidget(self._audio_button)

        self._quality_combo = QComboBox(self._content_page)
        self._quality_combo.currentIndexChanged.connect(self._on_quality_changed)
        self._output_combo = QComboBox(self._content_page)
        self._output_combo.currentIndexChanged.connect(self._on_output_changed)
        self._hint = muted_label(parent=self._content_page)

        self._add_button = icon_button(themed_icon("list-plus", ON_ACCENT), "Añadir a la cola", self._content_page)
        self._add_button.setProperty("variant", "primary")
        self._add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_button.clicked.connect(self._emit_download_request)

        self._status = muted_label(parent=self._content_page)
        self._retry_button = QPushButton("Reintentar", self._content_page)
        self._retry_button.clicked.connect(self.retry_requested)

        layout = QVBoxLayout(self._content_page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addWidget(self._thumbnail, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self._title)
        layout.addWidget(self._details)
        layout.addSpacing(6)
        layout.addWidget(section_title("Formato", self._content_page))
        layout.addLayout(segments)
        layout.addWidget(muted_label("Calidad", self._content_page))
        layout.addWidget(self._quality_combo)
        layout.addWidget(muted_label("Archivo de salida", self._content_page))
        layout.addWidget(self._output_combo)
        layout.addWidget(self._hint)
        layout.addStretch()
        layout.addWidget(self._status)
        layout.addWidget(self._retry_button)
        layout.addWidget(self._add_button)
        return self._content_page

    def _segment_button(self, text: str, icon_name: str) -> QPushButton:
        button = icon_button(themed_icon(icon_name, MUTED_TEXT, checked_color=ACCENT), text, self)
        button.setCheckable(True)
        button.setProperty("segment", "true")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def _select_initial_kind(self, metadata: VideoMetadata) -> None:
        prefers_audio = self._preferences.media_kind is MediaKind.AUDIO or not metadata.video_formats
        target = self._audio_button if prefers_audio and metadata.audio_formats else self._video_button
        if target.isChecked():
            self._populate_formats()
        else:
            target.setChecked(True)

    def _selected_kind(self) -> MediaKind:
        return MediaKind.AUDIO if self._audio_button.isChecked() else MediaKind.VIDEO

    def _on_kind_toggled(self, button: QPushButton, checked: bool) -> None:
        if checked and self._metadata is not None:
            self._preferences.media_kind = self._selected_kind()
            self._populate_formats()

    def _populate_formats(self) -> None:
        if self._metadata is None:
            return
        formats = self._metadata.audio_formats if self._selected_kind() is MediaKind.AUDIO else self._metadata.video_formats
        self._quality_combo.blockSignals(True)
        self._quality_combo.clear()
        for media_format in formats:
            self._quality_combo.addItem(media_format.label, media_format)
        self._quality_combo.blockSignals(False)
        self._on_quality_changed()

    def _on_quality_changed(self) -> None:
        selected = self._quality_combo.currentData()
        if isinstance(selected, VideoFormat):
            self._populate_containers(selected)
        elif isinstance(selected, AudioFormat):
            self._populate_audio_outputs()
        self._update_hint()

    def _populate_containers(self, video_format: VideoFormat) -> None:
        containers = video_format.compatible_containers
        self._replace_output_items([(container.upper(), container) for container in containers])
        preferred = self._preferences.video_container
        self._output_combo.setCurrentIndex(containers.index(preferred) if preferred in containers else 0)

    def _populate_audio_outputs(self) -> None:
        outputs = list(AudioOutput)
        self._replace_output_items([(output.label, output) for output in outputs])
        self._output_combo.setCurrentIndex(outputs.index(self._preferences.audio_output))

    def _replace_output_items(self, items: list[tuple[str, object]]) -> None:
        self._output_combo.blockSignals(True)
        self._output_combo.clear()
        for label, value in items:
            self._output_combo.addItem(label, value)
        self._output_combo.blockSignals(False)

    def _on_output_changed(self) -> None:
        selected = self._output_combo.currentData()
        if isinstance(selected, AudioOutput):
            self._preferences.audio_output = selected
        elif isinstance(selected, str):
            self._preferences.video_container = selected
        self._update_hint()

    def _update_hint(self) -> None:
        self._hint.setText(self._describe_selection())

    def _describe_selection(self) -> str:
        selected_format = self._quality_combo.currentData()
        output = self._output_combo.currentData()
        if isinstance(selected_format, VideoFormat):
            if selected_format.has_audio:
                return "Este formato ya incluye audio."
            return "Se combinará con la mejor pista de audio disponible usando FFmpeg."
        if isinstance(output, AudioOutput) and output.requires_conversion:
            return "El audio se convertirá con FFmpeg a máxima calidad."
        return "El audio se guardará tal cual, sin conversión."

    def _emit_download_request(self) -> None:
        if self._metadata is None:
            return
        request = self._build_request(self._metadata)
        if request is not None:
            self.download_requested.emit(request, self._metadata)

    def _build_request(self, metadata: VideoMetadata) -> DownloadRequest | None:
        selected_format = self._quality_combo.currentData()
        output = self._output_combo.currentData()
        destination = self._preferences.download_directory
        if isinstance(selected_format, VideoFormat) and isinstance(output, str):
            return VideoDownloadRequest(metadata.url, destination, selected_format, output)
        if isinstance(selected_format, AudioFormat) and isinstance(output, AudioOutput):
            return AudioDownloadRequest(metadata.url, destination, selected_format, output)
        return None

    def _set_form_enabled(self, enabled: bool) -> None:
        for widget in (self._quality_combo, self._output_combo, self._add_button):
            widget.setEnabled(enabled)
        if enabled:
            return
        self._video_button.setEnabled(False)
        self._audio_button.setEnabled(False)
        self._quality_combo.clear()
        self._output_combo.clear()
        self._hint.setText("")

    def _set_status(self, message: str, tone: str) -> None:
        self._status.setText(message)
        self._status.setVisible(bool(message))
        set_style_property(self._status, "tone", tone)
