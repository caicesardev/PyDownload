from functools import cache

from PySide6.QtCore import QByteArray, QFile, QIODevice, QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from src.widgets.theme import DISABLED_TEXT, TEXT

ICON_RESOURCE_TEMPLATE = ":/icons/{name}.svg"
CURRENT_COLOR = "currentColor"
UI_ICON_SIZES = (16, 20, 24, 32, 48)
APP_ICON_SIZES = (16, 24, 32, 48, 64, 128, 256)
LOGO = "logo"


def svg_pixmap(name: str, size: int, color: str | None = TEXT, device_pixel_ratio: float = 1.0) -> QPixmap:
    renderer = QSvgRenderer(QByteArray(_colored_svg(name, color).encode("utf-8")))
    pixmap = QPixmap(QSize(size, size) * device_pixel_ratio)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    pixmap.setDevicePixelRatio(device_pixel_ratio)
    return pixmap


@cache
def themed_icon(name: str, color: str = TEXT, checked_color: str | None = None) -> QIcon:
    icon = QIcon()
    for size in UI_ICON_SIZES:
        icon.addPixmap(svg_pixmap(name, size, color), QIcon.Mode.Normal, QIcon.State.Off)
        icon.addPixmap(svg_pixmap(name, size, DISABLED_TEXT), QIcon.Mode.Disabled, QIcon.State.Off)
        if checked_color is not None:
            icon.addPixmap(svg_pixmap(name, size, checked_color), QIcon.Mode.Normal, QIcon.State.On)
    return icon


@cache
def app_icon() -> QIcon:
    icon = QIcon()
    for size in APP_ICON_SIZES:
        icon.addPixmap(svg_pixmap(LOGO, size, color=None))
    return icon


def _colored_svg(name: str, color: str | None) -> str:
    source = _svg_source(name)
    return source if color is None else source.replace(CURRENT_COLOR, color)


@cache
def _svg_source(name: str) -> str:
    resource = QFile(ICON_RESOURCE_TEMPLATE.format(name=name))
    if not resource.open(QIODevice.OpenModeFlag.ReadOnly):
        raise FileNotFoundError(f"Icon resource not found: {name}")
    try:
        return bytes(resource.readAll().data()).decode("utf-8")
    finally:
        resource.close()
