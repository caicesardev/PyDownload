import unittest
from pathlib import Path

from src.models.download_request import AudioDownloadRequest, AudioOutput, MediaKind, VideoDownloadRequest
from src.models.media_format import AudioFormat, VideoFormat

URL = "https://www.youtube.com/watch?v=dP15zlyra3c"
DESTINATION = Path("downloads")
H264_VIDEO = VideoFormat("137", "mp4", "avc1.640028", 1080, 25, None, "SDR", has_audio=False)
VP9_VIDEO = VideoFormat("248", "webm", "vp9", 1080, 25, None, "SDR", has_audio=False)
PROGRESSIVE_VIDEO = VideoFormat("18", "mp4", "avc1.42001E", 360, 25, None, "SDR", has_audio=True)
OPUS_AUDIO = AudioFormat("251", "webm", "opus", 126, None, None)


class VideoDownloadRequestTest(unittest.TestCase):
    def test_merges_with_audio_matching_the_container(self) -> None:
        request = VideoDownloadRequest(URL, DESTINATION, H264_VIDEO, "mp4")
        self.assertEqual(request.ydl_options()["format"], "137+bestaudio[ext=m4a]/137+bestaudio")
        self.assertEqual(request.ydl_options()["merge_output_format"], "mp4")
        self.assertTrue(request.requires_ffmpeg)

    def test_accepts_any_audio_for_mkv(self) -> None:
        request = VideoDownloadRequest(URL, DESTINATION, VP9_VIDEO, "mkv")
        self.assertEqual(request.ydl_options()["format"], "248+bestaudio")

    def test_downloads_progressive_format_as_is(self) -> None:
        request = VideoDownloadRequest(URL, DESTINATION, PROGRESSIVE_VIDEO, "mp4")
        self.assertEqual(request.ydl_options()["format"], "18")
        self.assertFalse(request.requires_ffmpeg)

    def test_offers_only_containers_that_support_the_codec(self) -> None:
        self.assertEqual(H264_VIDEO.compatible_containers, ("mp4", "mkv"))
        self.assertEqual(VP9_VIDEO.compatible_containers, ("mp4", "webm", "mkv"))
        self.assertEqual(PROGRESSIVE_VIDEO.compatible_containers, ("mp4",))

    def test_summarises_the_selection(self) -> None:
        request = VideoDownloadRequest(URL, DESTINATION, H264_VIDEO, "mkv")
        self.assertEqual(request.summary, "Vídeo · 1080p · 25 fps · MP4 · H.264 → MKV")
        self.assertIs(request.kind, MediaKind.VIDEO)


class AudioDownloadRequestTest(unittest.TestCase):
    def test_converts_with_best_quality(self) -> None:
        request = AudioDownloadRequest(URL, DESTINATION, OPUS_AUDIO, AudioOutput.MP3)
        self.assertEqual(request.ydl_options()["postprocessors"], [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }])
        self.assertTrue(request.requires_ffmpeg)

    def test_keeps_original_stream_without_ffmpeg(self) -> None:
        request = AudioDownloadRequest(URL, DESTINATION, OPUS_AUDIO, AudioOutput.ORIGINAL)
        self.assertEqual(request.ydl_options(), {"format": "251"})
        self.assertFalse(request.requires_ffmpeg)

    def test_summarises_the_selection(self) -> None:
        request = AudioDownloadRequest(URL, DESTINATION, OPUS_AUDIO, AudioOutput.MP3)
        self.assertEqual(request.summary, "Audio · 126 kbps · WEBM · Opus → MP3")
        self.assertIs(request.kind, MediaKind.AUDIO)


if __name__ == "__main__":
    unittest.main()
