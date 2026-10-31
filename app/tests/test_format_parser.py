import unittest

from src.services.format_parser import parse_metadata

STORYBOARD = {"format_id": "sb0", "ext": "mhtml", "vcodec": "none", "acodec": "none", "protocol": "mhtml"}
HLS_AUDIO = {"format_id": "234", "ext": "mp4", "vcodec": "none", "acodec": None, "protocol": "m3u8_native"}
HLS_VIDEO = {"format_id": "270", "ext": "mp4", "vcodec": "avc1.640028", "acodec": "none", "height": 1080,
             "fps": 25.0, "protocol": "m3u8_native"}
AAC_AUDIO = {"format_id": "140", "ext": "m4a", "vcodec": "none", "acodec": "mp4a.40.2", "abr": 129.577,
             "filesize": 946257, "language": "en", "protocol": "https"}
DRC_AUDIO = {**AAC_AUDIO, "format_id": "140-drc"}
OPUS_AUDIO = {"format_id": "251", "ext": "webm", "vcodec": "none", "acodec": "opus", "abr": 125.627,
              "filesize": 916784, "language": "en", "protocol": "https"}
H264_1080 = {"format_id": "137", "ext": "mp4", "vcodec": "avc1.640028", "acodec": "none", "height": 1080,
             "fps": 25, "filesize": 18816948, "dynamic_range": "SDR", "protocol": "https"}
VP9_720 = {"format_id": "247", "ext": "webm", "vcodec": "vp9", "acodec": "none", "height": 720, "fps": 25,
           "filesize": 1717208, "dynamic_range": "SDR", "protocol": "https"}
PROGRESSIVE_360 = {"format_id": "18", "ext": "mp4", "vcodec": "avc1.42001E", "acodec": "mp4a.40.2", "height": 360,
                   "fps": 25, "filesize_approx": 2415109, "dynamic_range": "SDR", "protocol": "https"}

INFO = {
    "id": "dP15zlyra3c",
    "webpage_url": "https://www.youtube.com/watch?v=dP15zlyra3c",
    "title": "Fox Snow Dive - Yellowstone - BBC",
    "channel": "BBC",
    "duration": 58,
    "view_count": 1534200,
    "upload_date": "20140116",
    "formats": [STORYBOARD, HLS_AUDIO, HLS_VIDEO, DRC_AUDIO, OPUS_AUDIO, AAC_AUDIO, VP9_720, PROGRESSIVE_360,
                H264_1080],
}


class ParseMetadataTest(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata = parse_metadata(INFO)

    def test_reads_video_details(self) -> None:
        self.assertEqual(self.metadata.title, "Fox Snow Dive - Yellowstone - BBC")
        self.assertEqual(self.metadata.video_id, "dP15zlyra3c")
        self.assertEqual(self.metadata.details, "BBC · 0:58 · 1.5 M visualizaciones · 16/01/2014")
        self.assertEqual(self.metadata.thumbnail_url, "https://i.ytimg.com/vi/dP15zlyra3c/mqdefault.jpg")

    def test_lists_direct_video_formats_from_best_to_worst(self) -> None:
        self.assertEqual([video.format_id for video in self.metadata.video_formats], ["137", "247", "18"])

    def test_lists_audio_only_formats_without_drc_duplicates(self) -> None:
        self.assertEqual([audio.format_id for audio in self.metadata.audio_formats], ["140", "251"])

    def test_builds_readable_labels(self) -> None:
        self.assertEqual(self.metadata.video_formats[0].label, "1080p · 25 fps · MP4 · H.264 · 17.9 MB")
        self.assertEqual(self.metadata.video_formats[2].label, "360p · 25 fps · MP4 · H.264 · 2.3 MB · con audio")
        self.assertEqual(self.metadata.audio_formats[0].label, "130 kbps · M4A · AAC · 924.1 KB")

    def test_hides_language_when_every_track_shares_it(self) -> None:
        self.assertTrue(all(audio.language is None for audio in self.metadata.audio_formats))

    def test_falls_back_to_streaming_formats_when_no_direct_ones_exist(self) -> None:
        metadata = parse_metadata({**INFO, "formats": [HLS_VIDEO]})
        self.assertEqual([video.format_id for video in metadata.video_formats], ["270"])

    def test_reports_missing_formats(self) -> None:
        self.assertFalse(parse_metadata({**INFO, "formats": [STORYBOARD]}).has_formats)


if __name__ == "__main__":
    unittest.main()
