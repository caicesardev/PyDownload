from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.widgets.labels import muted_label, section_title

DEFAULT_ILLUSTRATION_WIDTH = 220
TEXT_MAX_WIDTH = 360


class EmptyState(QWidget):
    def __init__(
        self,
        illustration: str,
        title: str,
        description: str,
        parent: QWidget | None = None,
        illustration_width: int = DEFAULT_ILLUSTRATION_WIDTH,
    ) -> None:
        super().__init__(parent)
        image = QLabel(self)
        image.setPixmap(QPixmap(illustration).scaledToWidth(illustration_width, Qt.TransformationMode.SmoothTransformation))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        heading = section_title(title, self)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body = muted_label(description, self)
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setMaximumWidth(TEXT_MAX_WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)
        layout.addStretch()
        layout.addWidget(image)
        layout.addWidget(heading)
        layout.addWidget(body)
        layout.addStretch()
