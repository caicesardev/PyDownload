from dataclasses import dataclass

from src.utils.formatting import format_bytes, friendly_codec_name

H264_CODEC_FAMILIES = ("avc1", "avc3")
SEPARATOR = " · "


@dataclass(frozen=True)
class VideoFormat:
    format_id: str
    extension: str
    codec: str
    height: int
    fps: int
    filesize: int | None
    dynamic_range: str
    has_audio: bool

    @property
    def label(self) -> str:
        parts = [f"{self.height}p" if self.height else "?"]
        if self.fps:
            parts.append(f"{self.fps} fps")
        if self.dynamic_range != "SDR":
            parts.append(self.dynamic_range)
        parts.append(self.extension.upper())
        parts.append(friendly_codec_name(self.codec))
        if self.filesize:
            parts.append(format_bytes(self.filesize))
        if self.has_audio:
            parts.append("con audio")
        return SEPARATOR.join(parts)

    @property
    def compatible_containers(self) -> tuple[str, ...]:
        if self.has_audio:
            return (self.extension,)
        if self.codec.lower().startswith(H264_CODEC_FAMILIES):
            return ("mp4", "mkv")
        return ("mp4", "webm", "mkv")


@dataclass(frozen=True)
class AudioFormat:
    format_id: str
    extension: str
    codec: str
    bitrate: int
    filesize: int | None
    language: str | None

    @property
    def label(self) -> str:
        parts = [f"{self.bitrate} kbps" if self.bitrate else "?"]
        parts.append(self.extension.upper())
        parts.append(friendly_codec_name(self.codec))
        if self.filesize:
            parts.append(format_bytes(self.filesize))
        if self.language:
            parts.append(self.language.upper())
        return SEPARATOR.join(parts)
