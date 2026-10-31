from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget

ICON_TEXT_GAP = " "


def icon_button(icon: QIcon, text: str, parent: QWidget | None = None) -> QPushButton:
    return QPushButton(icon, f"{ICON_TEXT_GAP}{text}", parent)
