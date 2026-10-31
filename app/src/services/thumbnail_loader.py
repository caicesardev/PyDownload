from urllib.parse import urlsplit

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

THUMBNAIL_HOST_SUFFIX = ".ytimg.com"
MAX_THUMBNAIL_BYTES = 4 * 1024 * 1024
TRANSFER_TIMEOUT_MILLISECONDS = 15_000


def is_trusted_thumbnail_url(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    return parts.scheme == "https" and host.endswith(THUMBNAIL_HOST_SUFFIX)


class ThumbnailLoader(QObject):
    thumbnail_ready = Signal(str, QPixmap)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._network = QNetworkAccessManager(self)
        self._cache: dict[str, QPixmap] = {}
        self._in_flight: set[str] = set()

    def load(self, url: str) -> None:
        if cached := self._cache.get(url):
            self.thumbnail_ready.emit(url, cached)
            return
        if url in self._in_flight or not is_trusted_thumbnail_url(url):
            return
        request = QNetworkRequest(QUrl(url))
        request.setTransferTimeout(TRANSFER_TIMEOUT_MILLISECONDS)
        reply = self._network.get(request)
        self._in_flight.add(url)
        reply.finished.connect(lambda: self._on_reply_finished(url, reply))

    def _on_reply_finished(self, url: str, reply: QNetworkReply) -> None:
        self._in_flight.discard(url)
        reply.deleteLater()
        if reply.error() is not QNetworkReply.NetworkError.NoError:
            return
        payload = reply.read(MAX_THUMBNAIL_BYTES)
        pixmap = QPixmap()
        if pixmap.loadFromData(payload):
            self._cache[url] = pixmap
            self.thumbnail_ready.emit(url, pixmap)
