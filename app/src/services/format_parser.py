from typing import Any

from src.models.media_format import AudioFormat, VideoFormat
from src.models.video_metadata import VideoMetadata

NO_CODEC = "none"
STREAMING_PROTOCOL_PREFIX = "m3u8"
DYNAMIC_RANGE_COMPRESSION_SUFFIX = "-drc"

RawFormat = dict[str, Any]


def parse_metadata(info: dict[str, Any]) -> VideoMetadata:
    formats = _downloadable_formats(info.get("formats") or [])
    return VideoMetadata(
        video_id=info.get("id") or "",
        url=info.get("webpage_url") or info.get("original_url") or "",
        title=info.get("title") or "",
        channel=info.get("channel") or info.get("uploader") or "",
        duration=int(info.get("duration") or 0),
        view_count=int(info.get("view_count") or 0),
        upload_date=info.get("upload_date") or "",
        video_formats=_parse_video_formats(formats),
        audio_formats=_parse_audio_formats(formats),
    )


def _downloadable_formats(formats: list[RawFormat]) -> list[RawFormat]:
    media_formats = [
        raw for raw in formats
        if (_has_video(raw) or _has_audio(raw)) and not _is_dynamic_range_compressed(raw)
    ]
    direct_formats = [raw for raw in media_formats if not _is_streaming_manifest(raw)]
    return direct_formats or media_formats


def _parse_video_formats(formats: list[RawFormat]) -> tuple[VideoFormat, ...]:
    video_formats = [_to_video_format(raw) for raw in formats if _has_video(raw)]
    return tuple(sorted(
        video_formats,
        key=lambda video: (video.height, video.fps, video.filesize or 0),
        reverse=True,
    ))


def _parse_audio_formats(formats: list[RawFormat]) -> tuple[AudioFormat, ...]:
    audio_only_formats = [raw for raw in formats if _has_audio(raw) and not _has_video(raw)]
    show_language = len({raw.get("language") for raw in audio_only_formats}) > 1
    audio_formats = [_to_audio_format(raw, show_language) for raw in audio_only_formats]
    return tuple(sorted(
        audio_formats,
        key=lambda audio: (audio.bitrate, audio.filesize or 0),
        reverse=True,
    ))


def _to_video_format(raw: RawFormat) -> VideoFormat:
    return VideoFormat(
        format_id=raw["format_id"],
        extension=raw.get("ext") or "",
        codec=raw.get("vcodec") or "",
        height=int(raw.get("height") or 0),
        fps=round(raw.get("fps") or 0),
        filesize=_filesize(raw),
        dynamic_range=raw.get("dynamic_range") or "SDR",
        has_audio=_has_audio(raw),
    )


def _to_audio_format(raw: RawFormat, show_language: bool) -> AudioFormat:
    return AudioFormat(
        format_id=raw["format_id"],
        extension=raw.get("ext") or "",
        codec=raw.get("acodec") or "",
        bitrate=round(raw.get("abr") or raw.get("tbr") or 0),
        filesize=_filesize(raw),
        language=raw.get("language") if show_language else None,
    )


def _has_video(raw: RawFormat) -> bool:
    return raw.get("vcodec") not in (None, NO_CODEC)


def _has_audio(raw: RawFormat) -> bool:
    return raw.get("acodec") not in (None, NO_CODEC)


def _is_dynamic_range_compressed(raw: RawFormat) -> bool:
    return str(raw.get("format_id", "")).endswith(DYNAMIC_RANGE_COMPRESSION_SUFFIX)


def _is_streaming_manifest(raw: RawFormat) -> bool:
    return str(raw.get("protocol", "")).startswith(STREAMING_PROTOCOL_PREFIX)


def _filesize(raw: RawFormat) -> int | None:
    return raw.get("filesize") or raw.get("filesize_approx")
