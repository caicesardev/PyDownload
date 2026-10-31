from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from src.services.ffmpeg_locator import locate_ffmpeg
from src.settings.preferences import MAX_CONCURRENT_DOWNLOADS_LIMIT, Preferences
from src.widgets.buttons import icon_button
from src.widgets.labels import muted_label, page_title, section_title
from src.widgets.icons import themed_icon
from src.widgets.theme import DANGER, set_style_property

MAX_RATE_LIMIT_KIB = 1_000_000
NUMBER_INPUT_WIDTH = 160
FFMPEG_FILE_FILTER = "FFmpeg (ffmpeg.exe ffmpeg);;Todos los archivos (*)"


class SettingsPage(QWidget):
    settings_saved = Signal()
    clear_browsing_data_requested = Signal()

    def __init__(self, preferences: Preferences, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Page")
        self._preferences = preferences

        self._directory_input = QLineEdit(self)
        self._directory_input.setReadOnly(True)
        self._concurrency_input = QSpinBox(self)
        self._concurrency_input.setRange(1, MAX_CONCURRENT_DOWNLOADS_LIMIT)
        self._rate_limit_input = QSpinBox(self)
        self._rate_limit_input.setRange(0, MAX_RATE_LIMIT_KIB)
        self._rate_limit_input.setSingleStep(256)
        self._rate_limit_input.setSuffix(" KB/s")
        self._rate_limit_input.setSpecialValueText("Sin límite")
        for number_input in (self._concurrency_input, self._rate_limit_input):
            number_input.setMaximumWidth(NUMBER_INPUT_WIDTH)
        self._ffmpeg_input = QLineEdit(self)
        self._ffmpeg_input.setPlaceholderText("Automático (FFmpeg incluido)")
        self._ffmpeg_input.textChanged.connect(self._describe_ffmpeg)
        self._ffmpeg_status = muted_label(parent=self)
        self._save_status = muted_label(parent=self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(page_title("Ajustes", self))
        layout.addWidget(self._build_downloads_card())
        layout.addWidget(self._build_browser_card())
        layout.addStretch()
        layout.addLayout(self._build_footer())
        self.load()

    def load(self) -> None:
        self._directory_input.setText(str(self._preferences.download_directory))
        self._concurrency_input.setValue(self._preferences.max_concurrent_downloads)
        self._rate_limit_input.setValue(self._preferences.rate_limit_kib)
        self._ffmpeg_input.setText(self._preferences.ffmpeg_location)
        self._describe_ffmpeg()
        self._save_status.clear()

    def _build_downloads_card(self) -> QFrame:
        card = QFrame(self)
        card.setObjectName("Card")
        browse_directory = icon_button(themed_icon("folder-open"), "Examinar…", card)
        browse_directory.clicked.connect(self._choose_directory)
        browse_ffmpeg = icon_button(themed_icon("folder-open"), "Examinar…", card)
        browse_ffmpeg.clicked.connect(self._choose_ffmpeg)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setHorizontalSpacing(24)
        form.setVerticalSpacing(12)
        form.addRow("Carpeta de descargas", self._row(self._directory_input, browse_directory))
        form.addRow("Descargas simultáneas", self._concurrency_input)
        form.addRow("Límite de velocidad por descarga", self._rate_limit_input)
        form.addRow("Ubicación de FFmpeg", self._row(self._ffmpeg_input, browse_ffmpeg))
        form.addRow("", self._ffmpeg_status)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(section_title("Descargas", card))
        layout.addLayout(form)
        return card

    def _build_browser_card(self) -> QFrame:
        card = QFrame(self)
        card.setObjectName("Card")
        clear_button = icon_button(themed_icon("trash-2", DANGER), "Borrar cookies y caché", card)
        clear_button.setProperty("variant", "danger")
        clear_button.clicked.connect(self._confirm_clear_browsing_data)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        layout.addWidget(section_title("Navegador", card))
        layout.addWidget(muted_label(
            "El navegador integrado solo permite YouTube y el inicio de sesión de Google. "
            "Los permisos (cámara, micrófono, ubicación, notificaciones) se deniegan siempre y "
            "las cookies nunca se comparten con el motor de descargas.",
            card,
        ))
        layout.addWidget(clear_button, alignment=Qt.AlignmentFlag.AlignLeft)
        return card

    def _build_footer(self) -> QHBoxLayout:
        restore_button = QPushButton("Descartar cambios", self)
        restore_button.clicked.connect(self.load)
        save_button = QPushButton("Guardar cambios", self)
        save_button.setProperty("variant", "primary")
        save_button.clicked.connect(self._save)

        footer = QHBoxLayout()
        footer.addWidget(self._save_status, stretch=1)
        footer.addWidget(restore_button)
        footer.addWidget(save_button)
        return footer

    @staticmethod
    def _row(field: QWidget, button: QPushButton) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addWidget(field, stretch=1)
        row.addWidget(button)
        return row

    def _choose_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Carpeta de descargas", self._directory_input.text())
        if directory:
            self._directory_input.setText(str(Path(directory)))

    def _choose_ffmpeg(self) -> None:
        file_path, _selected_filter = QFileDialog.getOpenFileName(self, "Ejecutable de FFmpeg", "", FFMPEG_FILE_FILTER)
        if file_path:
            self._ffmpeg_input.setText(str(Path(file_path)))

    def _describe_ffmpeg(self) -> None:
        custom_location = self._ffmpeg_input.text().strip()
        resolved = locate_ffmpeg(custom_location)
        if custom_location and resolved != custom_location:
            self._ffmpeg_status.setText("La ruta indicada no existe; se usará la detección automática.")
            set_style_property(self._ffmpeg_status, "tone", "warning")
        elif resolved:
            self._ffmpeg_status.setText(f"FFmpeg disponible: {resolved}")
            set_style_property(self._ffmpeg_status, "tone", "success")
        else:
            self._ffmpeg_status.setText("FFmpeg no encontrado: no se podrá unir vídeo y audio ni convertir audio.")
            set_style_property(self._ffmpeg_status, "tone", "error")

    def _save(self) -> None:
        self._preferences.download_directory = Path(self._directory_input.text())
        self._preferences.max_concurrent_downloads = self._concurrency_input.value()
        self._preferences.rate_limit_kib = self._rate_limit_input.value()
        self._preferences.ffmpeg_location = self._ffmpeg_input.text()
        self._save_status.setText("Cambios guardados. Se aplican a las próximas descargas.")
        set_style_property(self._save_status, "tone", "success")
        self.settings_saved.emit()

    def _confirm_clear_browsing_data(self) -> None:
        answer = QMessageBox.question(
            self,
            "Borrar datos del navegador",
            "Se cerrará la sesión de YouTube y se borrarán las cookies y la caché. ¿Continuar?",
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.clear_browsing_data_requested.emit()
            self._save_status.setText("Datos del navegador borrados.")
            set_style_property(self._save_status, "tone", "success")
