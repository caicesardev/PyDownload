from dataclasses import dataclass

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QButtonGroup, QFrame, QLabel, QSizePolicy, QToolButton, QVBoxLayout, QWidget

SIDEBAR_WIDTH = 104
ICON_SIZE = QSize(30, 30)
LOGO_SIZE = 44


@dataclass(frozen=True)
class SidebarEntry:
    label: str
    icon: str


class Sidebar(QFrame):
    page_selected = Signal(int)

    def __init__(self, entries: list[SidebarEntry], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        self._entries = entries
        self._buttons: list[QToolButton] = []
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._group.idClicked.connect(self.page_selected)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(6)
        layout.addWidget(self._create_logo(), alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(12)
        for index, entry in enumerate(entries):
            button = self._create_button(entry)
            self._group.addButton(button, index)
            self._buttons.append(button)
            layout.addWidget(button)
        layout.addStretch()
        self.select(0)

    def select(self, index: int) -> None:
        self._buttons[index].setChecked(True)

    def set_badge(self, index: int, count: int) -> None:
        label = self._entries[index].label
        self._buttons[index].setText(f"{label} ({count})" if count else label)

    def _create_logo(self) -> QLabel:
        logo = QLabel(self)
        logo.setPixmap(QPixmap(":/icons/app.png").scaled(
            LOGO_SIZE, LOGO_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation,
        ))
        return logo

    def _create_button(self, entry: SidebarEntry) -> QToolButton:
        button = QToolButton(self)
        button.setObjectName("SidebarButton")
        button.setText(entry.label)
        button.setIcon(QIcon(entry.icon))
        button.setIconSize(ICON_SIZE)
        button.setCheckable(True)
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button
