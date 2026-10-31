import re
from urllib.parse import parse_qs, quote_plus, urlsplit

VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")
YOUTUBE_HOSTS = ("youtube.com", "youtube-nocookie.com")
SHORT_LINK_HOST = "youtu.be"
PATH_PREFIXES_WITH_ID = ("shorts", "embed", "live", "v")
WATCH_URL_TEMPLATE = "https://www.youtube.com/watch?v={video_id}"
SEARCH_URL_TEMPLATE = "https://www.youtube.com/results?search_query={query}"
THUMBNAIL_URL_TEMPLATE = "https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"


def extract_video_id(url: str) -> str | None:
    parts = urlsplit(url.strip())
    if parts.scheme not in ("http", "https"):
        return None
    host = (parts.hostname or "").lower()
    path_segments = [segment for segment in parts.path.split("/") if segment]
    if host == SHORT_LINK_HOST:
        return _valid_video_id(path_segments[0] if path_segments else "")
    if not _is_youtube_host(host):
        return None
    if path_segments == ["watch"]:
        return _valid_video_id(parse_qs(parts.query).get("v", [""])[0])
    if len(path_segments) >= 2 and path_segments[0] in PATH_PREFIXES_WITH_ID:
        return _valid_video_id(path_segments[1])
    return None


def canonical_watch_url(video_id: str) -> str:
    return WATCH_URL_TEMPLATE.format(video_id=video_id)


def thumbnail_url(video_id: str) -> str:
    return THUMBNAIL_URL_TEMPLATE.format(video_id=video_id)


def search_url(query: str) -> str:
    return SEARCH_URL_TEMPLATE.format(query=quote_plus(query.strip()))


def is_youtube_url(url: str) -> bool:
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    return parts.scheme in ("http", "https") and (host == SHORT_LINK_HOST or _is_youtube_host(host))


def _is_youtube_host(host: str) -> bool:
    return any(host == domain or host.endswith(f".{domain}") for domain in YOUTUBE_HOSTS)


def _valid_video_id(candidate: str) -> str | None:
    return candidate if VIDEO_ID_PATTERN.match(candidate) else None
