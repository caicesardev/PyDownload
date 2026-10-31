from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

from src.models.media_format import AudioFormat, VideoFormat

PREFERRED_AUDIO_EXTENSION_BY_CONTAINER = {"mp4": "m4a", "webm": "webm"}
BEST_AUDIO_QUALITY = "0"


class MediaKind(Enum):
    VIDEO = "video"
    AUDIO = "audio"


class AudioOutput(Enum):
    MP3 = ("mp3", "MP3")
    M4A = ("m4a", "M4A (AAC)")
    OPUS = ("opus", "Opus")
    FLAC = ("flac", "FLAC (sin pérdida)")
    WAV = ("wav", "WAV (sin pérdida)")
    ORIGINAL = (None, "Original (sin conversión)")

    def __init__(self, codec: str | None, label: str) -> None:
        self.codec = codec
        self.label = label

    @property
    def requires_conversion(self) -> bool:
        return self.codec is not None


class DownloadRequest(Protocol):
    @property
    def url(self) -> str: ...

    @property
    def destination(self) -> Path: ...

    @property
    def kind(self) -> MediaKind: ...

    @property
    def summary(self) -> str: ...

    @property
    def requires_ffmpeg(self) -> bool: ...

    def ydl_options(self) -> dict[str, Any]: ...


@dataclass(frozen=True)
class VideoDownloadRequest:
    url: str
    destination: Path
    video_format: VideoFormat
    container: str

    @property
    def kind(self) -> MediaKind:
        return MediaKind.VIDEO

    @property
    def summary(self) -> str:
        return f"Vídeo · {self.video_format.label} → {self.container.upper()}"

    @property
    def requires_ffmpeg(self) -> bool:
        return not self.video_format.has_audio

    def ydl_options(self) -> dict[str, Any]:
        return {
            "format": self._format_selector(),
            "merge_output_format": self.container,
        }

    def _format_selector(self) -> str:
        video_id = self.video_format.format_id
        if self.video_format.has_audio:
            return video_id
        any_audio = f"{video_id}+bestaudio"
        preferred_extension = PREFERRED_AUDIO_EXTENSION_BY_CONTAINER.get(self.container)
        if preferred_extension is None:
            return any_audio
        return f"{video_id}+bestaudio[ext={preferred_extension}]/{any_audio}"


@dataclass(frozen=True)
class AudioDownloadRequest:
    url: str
    destination: Path
    audio_format: AudioFormat
    output: AudioOutput

    @property
    def kind(self) -> MediaKind:
        return MediaKind.AUDIO

    @property
    def summary(self) -> str:
        return f"Audio · {self.audio_format.label} → {self.output.label}"

    @property
    def requires_ffmpeg(self) -> bool:
        return self.output.requires_conversion

    def ydl_options(self) -> dict[str, Any]:
        options: dict[str, Any] = {"format": self.audio_format.format_id}
        if self.output.requires_conversion:
            options["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": self.output.codec,
                "preferredquality": BEST_AUDIO_QUALITY,
            }]
        return options
