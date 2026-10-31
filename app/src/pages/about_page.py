from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from constants import APP_NAME, REPOSITORY_URL, VERSION
from src.widgets.icons import LOGO, svg_pixmap
from src.widgets.labels import muted_label, page_title

LOGO_SIZE = 96
CARD_MAX_WIDTH = 560


class AboutPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Page")

        card = QFrame(self)
        card.setObjectName("Card")
        card.setMaximumWidth(CARD_MAX_WIDTH)

        logo = QLabel(card)
        logo.setPixmap(svg_pixmap(LOGO, LOGO_SIZE, color=None, device_pixel_ratio=self.devicePixelRatioF()))
        title = page_title(APP_NAME, card)
        version = muted_label(f"Versión {VERSION}", card)
        description = muted_label(
            "Navega por YouTube con un navegador integrado y protegido, consulta todos los formatos "
            "de vídeo y audio disponibles y descárgalos con un gestor de colas que nunca bloquea la interfaz.",
            card,
        )
        disclaimer = muted_label(
            "Proyecto educativo y sin ánimo de lucro, publicado bajo licencia MIT. "
            "Respeta los derechos de autor y los términos de servicio de YouTube.",
            card,
        )
        credits = QLabel(
            f'Hecho con <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a>, '
            f'<a href="https://doc.qt.io/qtforpython-6/">Qt for Python</a> y '
            f'<a href="https://ffmpeg.org/">FFmpeg</a>.<br>'
            f'Código fuente: <a href="{REPOSITORY_URL}">{REPOSITORY_URL}</a>',
            card,
        )
        credits.setOpenExternalLinks(True)
        credits.setTextFormat(Qt.TextFormat.RichText)
        credits.setWordWrap(True)
        about_qt = QPushButton("Acerca de Qt", card)
        about_qt.clicked.connect(QApplication.aboutQt)

        for label in (title, version, description, disclaimer, credits):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(10)
        card_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignHCenter)
        card_layout.addWidget(title)
        card_layout.addWidget(version)
        card_layout.addSpacing(8)
        card_layout.addWidget(description)
        card_layout.addWidget(disclaimer)
        card_layout.addWidget(credits)
        card_layout.addWidget(about_qt, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
