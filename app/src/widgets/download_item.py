from enum import Enum, auto

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.models.download_job import DownloadJob, DownloadState
from src.widgets.labels import muted_label, show_scaled_pixmap, thumbnail_label
from src.widgets.icons import themed_icon
from src.widgets.theme import DANGER, set_style_property

THUMBNAIL_WIDTH = 128
THUMBNAIL_HEIGHT = 72
ACTION_ICON_SIZE = QSize(18, 18)
PROGRESS_RESOLUTION = 1000
STATE_TONES = {
    DownloadState.COMPLETED: "success",
    DownloadState.FAILED: "error",
    DownloadState.CANCELLED: "warning",
}


class DownloadAction(Enum):
    PAUSE = auto()
    RESUME = auto()
    RETRY = auto()
    CANCEL = auto()
    OPEN_FOLDER = auto()
    REMOVE = auto()


class DownloadItem(QFrame):
    action_requested = Signal(int, object)

    def __init__(self, job: DownloadJob, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self._job_id = job.job_id

        self._thumbnail = thumbnail_label(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, self)
        self._title = QLabel(job.title, self)
        self._title.setObjectName("ItemTitle")
        self._title.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self._title.setToolTip(job.title)
        self._summary = muted_label(job.request.summary, self)
        self._progress = QProgressBar(self)
        self._progress.setTextVisible(False)
        self._status = muted_label(parent=self)

        self._buttons = {
            DownloadAction.PAUSE: self._action_button(themed_icon("pause"), "Pausar"),
            DownloadAction.RESUME: self._action_button(themed_icon("play"), "Reanudar"),
            DownloadAction.RETRY: self._action_button(themed_icon("rotate-ccw"), "Reintentar"),
            DownloadAction.CANCEL: self._action_button(themed_icon("x", DANGER), "Cancelar y borrar archivos parciales"),
            DownloadAction.OPEN_FOLDER: self._action_button(themed_icon("folder-open"), "Mostrar en la carpeta"),
            DownloadAction.REMOVE: self._action_button(themed_icon("trash-2"), "Quitar de la lista"),
        }
        for action, button in self._buttons.items():
            button.clicked.connect(lambda _checked=False, chosen=action: self.action_requested.emit(self._job_id, chosen))

        details = QVBoxLayout()
        details.setSpacing(4)
        details.addWidget(self._title)
        details.addWidget(self._summary)
        details.addWidget(self._progress)
        details.addWidget(self._status)

        actions = QHBoxLayout()
        actions.setSpacing(2)
        for button in self._buttons.values():
            actions.addWidget(button)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(14)
        layout.addWidget(self._thumbnail)
        layout.addLayout(details, stretch=1)
        layout.addLayout(actions)

        self.update_from(job)

    def set_thumbnail(self, pixmap: QPixmap) -> None:
        show_scaled_pixmap(self._thumbnail, pixmap)

    def update_from(self, job: DownloadJob) -> None:
        self._update_progress(job)
        self._update_status(job)
        self._buttons[DownloadAction.PAUSE].setVisible(job.can_pause)
        self._buttons[DownloadAction.RESUME].setVisible(job.can_resume)
        self._buttons[DownloadAction.RETRY].setVisible(job.can_retry)
        self._buttons[DownloadAction.CANCEL].setVisible(job.can_cancel)
        self._buttons[DownloadAction.OPEN_FOLDER].setVisible(job.state is DownloadState.COMPLETED)
        self._buttons[DownloadAction.REMOVE].setVisible(job.is_finished)

    def _update_progress(self, job: DownloadJob) -> None:
        is_busy = job.state is DownloadState.RUNNING and (job.progress == 0 or not job.cancellable)
        self._progress.setRange(0, 0 if is_busy else PROGRESS_RESOLUTION)
        self._progress.setValue(round(job.progress * PROGRESS_RESOLUTION / 100))
        self._progress.setVisible(job.state is not DownloadState.CANCELLED)

    def _update_status(self, job: DownloadJob) -> None:
        text = job.state.label
        if job.detail:
            text = job.detail if job.state is DownloadState.RUNNING else f"{text} · {job.detail}"
        self._status.setText(text)
        self._status.setToolTip(job.error or job.filepath or job.detail)
        set_style_property(self._status, "tone", STATE_TONES.get(job.state, ""))

    def _action_button(self, icon: QIcon, tooltip: str) -> QToolButton:
        button = QToolButton(self)
        button.setObjectName("ActionButton")
        button.setIcon(icon)
        button.setIconSize(ACTION_ICON_SIZE)
        button.setToolTip(tooltip)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button
