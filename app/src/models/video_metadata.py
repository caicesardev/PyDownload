from dataclasses import dataclass

from src.models.media_format import AudioFormat, VideoFormat
from src.services.youtube_url import thumbnail_url
from src.utils.formatting import format_count, format_duration, format_upload_date

SEPARATOR = " · "


@dataclass(frozen=True)
class VideoMetadata:
    video_id: str
    url: str
    title: str
    channel: str
    duration: int
    view_count: int
    upload_date: str
    video_formats: tuple[VideoFormat, ...]
    audio_formats: tuple[AudioFormat, ...]

    @property
    def thumbnail_url(self) -> str:
        return thumbnail_url(self.video_id)

    @property
    def has_formats(self) -> bool:
        return bool(self.video_formats or self.audio_formats)

    @property
    def details(self) -> str:
        parts = [self.channel] if self.channel else []
        if self.duration:
            parts.append(format_duration(self.duration))
        if self.view_count:
            parts.append(f"{format_count(self.view_count)} visualizaciones")
        if published := format_upload_date(self.upload_date):
            parts.append(published)
        return SEPARATOR.join(parts)
