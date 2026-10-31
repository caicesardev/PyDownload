from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QStyleFactory, QWidget

BACKGROUND = "#F4F5F7"
SURFACE = "#FFFFFF"
SURFACE_HOVER = "#EEF6F1"
BORDER = "#E1E4E8"
TEXT = "#1F2328"
MUTED_TEXT = "#6B7280"
DISABLED_TEXT = "#9CA3AF"
ACCENT = "#1E7F4F"
ACCENT_HOVER = "#17663F"
ACCENT_SOFT = "#DCEFE4"
DANGER = "#B42318"
ON_ACCENT = "#FFFFFF"
WARNING = "#B54708"

APP_STYLESHEET = f"""
QMainWindow, QWidget#Page {{
    background: {BACKGROUND};
}}
QWidget {{
    color: {TEXT};
    font-size: 13px;
}}
QFrame#Sidebar {{
    background: {SURFACE};
    border-right: 1px solid {BORDER};
}}
QToolButton#SidebarButton {{
    border: none;
    border-radius: 8px;
    padding: 8px 4px;
    color: {MUTED_TEXT};
    font-size: 12px;
}}
QToolButton#SidebarButton:hover {{
    background: {SURFACE_HOVER};
}}
QToolButton#SidebarButton:checked {{
    background: {ACCENT_SOFT};
    color: {ACCENT};
    font-weight: 600;
}}
QFrame#Card, QFrame#VideoPanel, QFrame#Toolbar {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
QLabel#PageTitle {{
    font-size: 22px;
    font-weight: 700;
}}
QLabel#SectionTitle {{
    font-size: 15px;
    font-weight: 600;
}}
QLabel#ItemTitle {{
    font-size: 14px;
    font-weight: 600;
}}
QLabel[muted="true"] {{
    color: {MUTED_TEXT};
}}
QLabel[tone="error"] {{
    color: {DANGER};
}}
QLabel[tone="warning"] {{
    color: {WARNING};
}}
QLabel[tone="success"] {{
    color: {ACCENT};
}}
QLabel#Thumbnail {{
    background: #E5E7EB;
    border-radius: 8px;
}}
QPushButton {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 14px;
}}
QPushButton:hover {{
    border-color: {ACCENT};
    background: {SURFACE_HOVER};
}}
QPushButton:disabled {{
    color: {DISABLED_TEXT};
    background: #F3F4F6;
}}
QPushButton[variant="primary"] {{
    background: {ACCENT};
    border-color: {ACCENT};
    color: white;
    font-weight: 600;
    padding: 8px 16px;
}}
QPushButton[variant="primary"]:hover {{
    background: {ACCENT_HOVER};
}}
QPushButton[variant="primary"]:disabled {{
    background: #A7C9B6;
    border-color: #A7C9B6;
}}
QPushButton[variant="danger"] {{
    color: {DANGER};
}}
QPushButton[segment="true"]:checked {{
    background: {ACCENT_SOFT};
    border-color: {ACCENT};
    color: {ACCENT};
    font-weight: 600;
}}
QToolButton#ActionButton {{
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 4px;
}}
QToolButton#ActionButton:hover {{
    border-color: {BORDER};
    background: {SURFACE_HOVER};
}}
QToolButton#NavigationButton {{
    border: none;
    border-radius: 6px;
    padding: 4px;
}}
QToolButton#NavigationButton:hover {{
    background: {SURFACE_HOVER};
}}
QLineEdit, QComboBox, QSpinBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 5px 8px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border-color: {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: url(:/icons/chevron-down-muted.svg);
    width: 14px;
    height: 14px;
}}
QSpinBox {{
    padding-right: 26px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    subcontrol-origin: border;
    width: 24px;
    border-left: 1px solid {BORDER};
    background: {SURFACE};
}}
QSpinBox::up-button {{
    subcontrol-position: top right;
    border-top-right-radius: 6px;
}}
QSpinBox::down-button {{
    subcontrol-position: bottom right;
    border-bottom-right-radius: 6px;
    border-top: 1px solid {BORDER};
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background: {SURFACE_HOVER};
}}
QSpinBox::up-arrow {{
    image: url(:/icons/chevron-up-muted.svg);
    width: 12px;
    height: 12px;
}}
QSpinBox::down-arrow {{
    image: url(:/icons/chevron-down-muted.svg);
    width: 12px;
    height: 12px;
}}
QMenu {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 6px;
}}
QMenu::item {{
    color: {TEXT};
    padding: 6px 28px 6px 12px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background: {ACCENT_SOFT};
    color: {TEXT};
}}
QMenu::item:disabled {{
    color: {DISABLED_TEXT};
}}
QMenu::icon {{
    padding-left: 8px;
}}
QMenu::separator {{
    height: 1px;
    background: {BORDER};
    margin: 4px 6px;
}}
QToolTip {{
    background: {TEXT};
    color: white;
    border: none;
    padding: 4px 8px;
}}
QLabel#EmptyStateIcon {{
    background: {ACCENT_SOFT};
    border-radius: 44px;
}}
QLineEdit#AddressBar {{
    border-radius: 16px;
    padding: 6px 14px;
    background: {BACKGROUND};
}}
QProgressBar {{
    background: #E5E7EB;
    border: none;
    border-radius: 4px;
    max-height: 8px;
}}
QProgressBar::chunk {{
    background: {ACCENT};
    border-radius: 4px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}
QTableWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    gridline-color: transparent;
    selection-background-color: {ACCENT_SOFT};
    selection-color: {TEXT};
}}
QHeaderView::section {{
    background: {SURFACE};
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 8px;
    font-weight: 600;
}}
QStatusBar {{
    background: {SURFACE};
    border-top: 1px solid {BORDER};
    color: {MUTED_TEXT};
}}
QSplitter::handle {{
    background: transparent;
}}
"""


def apply_theme(app: QApplication) -> None:
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    app.setStyle(QStyleFactory.create("Fusion"))
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.Link, QColor(ACCENT))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(ACCENT))
    app.setPalette(palette)
    app.setStyleSheet(APP_STYLESHEET)


def set_style_property(widget: QWidget, name: str, value: str) -> None:
    widget.setProperty(name, value)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
