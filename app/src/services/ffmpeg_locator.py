import shutil
from pathlib import Path

import imageio_ffmpeg


def locate_ffmpeg(custom_location: str) -> str | None:
    if custom_location and Path(custom_location).exists():
        return custom_location
    return shutil.which("ffmpeg") or _bundled_ffmpeg()


def _bundled_ffmpeg() -> str | None:
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except RuntimeError:
        return None
