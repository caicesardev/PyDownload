from typing import Any

from yt_dlp.utils import YoutubeDLError

SUPPORTED_JS_RUNTIMES = ("deno", "node", "bun")
ERROR_PREFIX = "ERROR: "
BYTES_PER_KIBIBYTE = 1024
SOCKET_TIMEOUT_SECONDS = 20
NETWORK_RETRIES = 10


def base_options(ffmpeg_location: str | None, rate_limit_kib: int = 0) -> dict[str, Any]:
    options: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "noplaylist": True,
        "color": "no_color",
        "socket_timeout": SOCKET_TIMEOUT_SECONDS,
        "retries": NETWORK_RETRIES,
        "fragment_retries": NETWORK_RETRIES,
        "js_runtimes": {runtime: {} for runtime in SUPPORTED_JS_RUNTIMES},
    }
    if ffmpeg_location:
        options["ffmpeg_location"] = ffmpeg_location
    if rate_limit_kib > 0:
        options["ratelimit"] = rate_limit_kib * BYTES_PER_KIBIBYTE
    return options


def describe_error(error: YoutubeDLError) -> str:
    return str(error).removeprefix(ERROR_PREFIX).strip()
