from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget


def page_title(text: str, parent: QWidget | None = None) -> QLabel:
    return _named_label(text, "PageTitle", parent)


def section_title(text: str, parent: QWidget | None = None) -> QLabel:
    return _named_label(text, "SectionTitle", parent)


def muted_label(text: str = "", parent: QWidget | None = None) -> QLabel:
    label = QLabel(text, parent)
    label.setProperty("muted", "true")
    label.setWordWrap(True)
    return label


def thumbnail_label(width: int, height: int, parent: QWidget | None = None) -> QLabel:
    label = QLabel(parent)
    label.setObjectName("Thumbnail")
    label.setFixedSize(width, height)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label


def show_scaled_pixmap(label: QLabel, pixmap: QPixmap) -> None:
    label.setPixmap(pixmap.scaled(
        label.size(),
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    ))


def _named_label(text: str, object_name: str, parent: QWidget | None) -> QLabel:
    label = QLabel(text, parent)
    label.setObjectName(object_name)
    label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    return label
