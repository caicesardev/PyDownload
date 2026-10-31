from pathlib import Path

from PySide6.QtCore import QByteArray, QSettings

from constants import APP_NAME, DEFAULT_DOWNLOAD_DIRECTORY
from src.models.download_request import AudioOutput, MediaKind

DOWNLOAD_DIRECTORY_KEY = "downloads/directory"
MAX_CONCURRENT_DOWNLOADS_KEY = "downloads/max_concurrent"
RATE_LIMIT_KEY = "downloads/rate_limit_kib"
FFMPEG_LOCATION_KEY = "downloads/ffmpeg_path"
MEDIA_KIND_KEY = "formats/media_kind"
VIDEO_CONTAINER_KEY = "formats/video_container"
AUDIO_OUTPUT_KEY = "formats/audio_output"
WINDOW_GEOMETRY_KEY = "window/geometry"

DEFAULT_MAX_CONCURRENT_DOWNLOADS = 2
MAX_CONCURRENT_DOWNLOADS_LIMIT = 5
DEFAULT_VIDEO_CONTAINER = "mp4"


class Preferences:
    def __init__(self) -> None:
        self._settings = QSettings(APP_NAME, "Preferences")

    @property
    def download_directory(self) -> Path:
        stored = str(self._settings.value(DOWNLOAD_DIRECTORY_KEY, "") or "")
        return Path(stored) if stored else DEFAULT_DOWNLOAD_DIRECTORY

    @download_directory.setter
    def download_directory(self, directory: Path) -> None:
        self._settings.setValue(DOWNLOAD_DIRECTORY_KEY, str(directory))

    @property
    def max_concurrent_downloads(self) -> int:
        stored = self._read_int(MAX_CONCURRENT_DOWNLOADS_KEY, DEFAULT_MAX_CONCURRENT_DOWNLOADS)
        return min(max(stored, 1), MAX_CONCURRENT_DOWNLOADS_LIMIT)

    @max_concurrent_downloads.setter
    def max_concurrent_downloads(self, count: int) -> None:
        self._settings.setValue(MAX_CONCURRENT_DOWNLOADS_KEY, count)

    @property
    def rate_limit_kib(self) -> int:
        return max(self._read_int(RATE_LIMIT_KEY, 0), 0)

    @rate_limit_kib.setter
    def rate_limit_kib(self, limit: int) -> None:
        self._settings.setValue(RATE_LIMIT_KEY, limit)

    @property
    def ffmpeg_location(self) -> str:
        return str(self._settings.value(FFMPEG_LOCATION_KEY, "") or "")

    @ffmpeg_location.setter
    def ffmpeg_location(self, location: str) -> None:
        self._settings.setValue(FFMPEG_LOCATION_KEY, location.strip())

    @property
    def media_kind(self) -> MediaKind:
        stored = str(self._settings.value(MEDIA_KIND_KEY, MediaKind.VIDEO.value))
        return MediaKind(stored) if stored in {kind.value for kind in MediaKind} else MediaKind.VIDEO

    @media_kind.setter
    def media_kind(self, kind: MediaKind) -> None:
        self._settings.setValue(MEDIA_KIND_KEY, kind.value)

    @property
    def video_container(self) -> str:
        return str(self._settings.value(VIDEO_CONTAINER_KEY, DEFAULT_VIDEO_CONTAINER) or DEFAULT_VIDEO_CONTAINER)

    @video_container.setter
    def video_container(self, container: str) -> None:
        self._settings.setValue(VIDEO_CONTAINER_KEY, container)

    @property
    def audio_output(self) -> AudioOutput:
        stored = str(self._settings.value(AUDIO_OUTPUT_KEY, AudioOutput.MP3.name))
        return AudioOutput[stored] if stored in AudioOutput.__members__ else AudioOutput.MP3

    @audio_output.setter
    def audio_output(self, output: AudioOutput) -> None:
        self._settings.setValue(AUDIO_OUTPUT_KEY, output.name)

    @property
    def window_geometry(self) -> QByteArray | None:
        geometry = self._settings.value(WINDOW_GEOMETRY_KEY)
        return geometry if isinstance(geometry, QByteArray) else None

    @window_geometry.setter
    def window_geometry(self, geometry: QByteArray) -> None:
        self._settings.setValue(WINDOW_GEOMETRY_KEY, geometry)

    def _read_int(self, key: str, default: int) -> int:
        try:
            return int(self._settings.value(key, default))
        except (TypeError, ValueError):
            return default
