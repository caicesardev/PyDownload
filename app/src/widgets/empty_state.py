from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.widgets.icons import svg_pixmap
from src.widgets.labels import muted_label, section_title
from src.widgets.theme import ACCENT

ICON_BADGE_SIZE = 88
ICON_SIZE = 40
TEXT_MAX_WIDTH = 360


class EmptyState(QWidget):
    def __init__(self, icon_name: str, title: str, description: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        badge = QLabel(self)
        badge.setObjectName("EmptyStateIcon")
        badge.setFixedSize(ICON_BADGE_SIZE, ICON_BADGE_SIZE)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setPixmap(svg_pixmap(icon_name, ICON_SIZE, ACCENT, self.devicePixelRatioF()))

        heading = section_title(title, self)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body = muted_label(description, self)
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setMaximumWidth(TEXT_MAX_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        layout.addStretch()
        layout.addLayout(self._centered_row(badge))
        layout.addLayout(self._centered_row(heading))
        layout.addLayout(self._centered_row(body, stretch=1))
        layout.addStretch()

    @staticmethod
    def _centered_row(widget: QWidget, stretch: int = 0) -> QHBoxLayout:
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(widget, stretch=stretch)
        row.addStretch()
        return row
