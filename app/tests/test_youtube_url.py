import unittest

from src.services.youtube_url import (
    canonical_watch_url,
    extract_video_id,
    is_youtube_url,
    search_url,
    thumbnail_url,
)

VIDEO_ID = "dP15zlyra3c"


class ExtractVideoIdTest(unittest.TestCase):
    def test_reads_watch_urls(self) -> None:
        self.assertEqual(extract_video_id(f"https://www.youtube.com/watch?v={VIDEO_ID}"), VIDEO_ID)
        self.assertEqual(extract_video_id(f"https://m.youtube.com/watch?v={VIDEO_ID}&t=42"), VIDEO_ID)

    def test_ignores_playlist_parameters(self) -> None:
        url = f"https://www.youtube.com/watch?v={VIDEO_ID}&list=PL123&index=4"
        self.assertEqual(extract_video_id(url), VIDEO_ID)

    def test_reads_short_links_shorts_and_embeds(self) -> None:
        self.assertEqual(extract_video_id(f"https://youtu.be/{VIDEO_ID}?si=abc"), VIDEO_ID)
        self.assertEqual(extract_video_id(f"https://www.youtube.com/shorts/{VIDEO_ID}"), VIDEO_ID)
        self.assertEqual(extract_video_id(f"https://www.youtube-nocookie.com/embed/{VIDEO_ID}"), VIDEO_ID)
        self.assertEqual(extract_video_id(f"https://www.youtube.com/live/{VIDEO_ID}"), VIDEO_ID)

    def test_rejects_pages_without_a_video(self) -> None:
        self.assertIsNone(extract_video_id("https://www.youtube.com/"))
        self.assertIsNone(extract_video_id("https://www.youtube.com/results?search_query=cats"))
        self.assertIsNone(extract_video_id("https://www.youtube.com/@channel/videos"))

    def test_rejects_lookalike_hosts_and_invalid_ids(self) -> None:
        self.assertIsNone(extract_video_id(f"https://youtube.com.evil.example/watch?v={VIDEO_ID}"))
        self.assertIsNone(extract_video_id(f"https://notyoutube.com/watch?v={VIDEO_ID}"))
        self.assertIsNone(extract_video_id("https://www.youtube.com/watch?v=short"))
        self.assertIsNone(extract_video_id("https://www.youtube.com/watch?v=../../etc/passwd"))
        self.assertIsNone(extract_video_id(f"javascript:alert('{VIDEO_ID}')"))


class UrlBuildersTest(unittest.TestCase):
    def test_builds_canonical_urls(self) -> None:
        self.assertEqual(canonical_watch_url(VIDEO_ID), f"https://www.youtube.com/watch?v={VIDEO_ID}")
        self.assertEqual(thumbnail_url(VIDEO_ID), f"https://i.ytimg.com/vi/{VIDEO_ID}/mqdefault.jpg")

    def test_encodes_search_queries(self) -> None:
        self.assertEqual(search_url(" lo-fi & chill "), "https://www.youtube.com/results?search_query=lo-fi+%26+chill")

    def test_recognises_youtube_urls(self) -> None:
        self.assertTrue(is_youtube_url("https://music.youtube.com/"))
        self.assertTrue(is_youtube_url(f"https://youtu.be/{VIDEO_ID}"))
        self.assertFalse(is_youtube_url("https://example.com/youtube.com"))


if __name__ == "__main__":
    unittest.main()
