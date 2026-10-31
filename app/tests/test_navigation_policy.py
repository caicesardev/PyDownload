import unittest

from src.browser.navigation_policy import (
    NavigationDecision,
    decide_embedded_frame_navigation,
    decide_main_frame_navigation,
    is_trusted_host,
)


class MainFrameNavigationTest(unittest.TestCase):
    def test_allows_youtube_over_https(self) -> None:
        for url in (
            "https://www.youtube.com/watch?v=dP15zlyra3c",
            "https://m.youtube.com/",
            "https://youtu.be/dP15zlyra3c",
            "https://accounts.google.com/signin",
            "https://accounts.google.es/accounts/SetSID",
            "https://consent.youtube.com/m",
        ):
            with self.subTest(url=url):
                self.assertIs(decide_main_frame_navigation(url, user_initiated=False), NavigationDecision.ALLOW)

    def test_blocks_plain_http_even_for_youtube(self) -> None:
        decision = decide_main_frame_navigation("http://www.youtube.com/", user_initiated=False)
        self.assertIs(decision, NavigationDecision.BLOCK)

    def test_sends_clicked_external_links_to_the_system_browser(self) -> None:
        decision = decide_main_frame_navigation("https://example.com/article", user_initiated=True)
        self.assertIs(decision, NavigationDecision.OPEN_EXTERNALLY)

    def test_blocks_external_redirects_and_scripts(self) -> None:
        self.assertIs(decide_main_frame_navigation("https://example.com/", user_initiated=False), NavigationDecision.BLOCK)
        self.assertIs(decide_main_frame_navigation("file:///C:/Windows/win.ini", user_initiated=True), NavigationDecision.BLOCK)
        self.assertIs(decide_main_frame_navigation("javascript:alert(1)", user_initiated=True), NavigationDecision.BLOCK)

    def test_rejects_lookalike_hosts(self) -> None:
        self.assertFalse(is_trusted_host("youtube.com.evil.example"))
        self.assertFalse(is_trusted_host("evilyoutube.com"))
        self.assertFalse(is_trusted_host("accounts.google.evil.com"))
        self.assertTrue(is_trusted_host("WWW.YOUTUBE.COM."))


class EmbeddedFrameNavigationTest(unittest.TestCase):
    def test_allows_secure_and_inline_frames(self) -> None:
        for url in ("https://www.google.com/recaptcha", "about:blank", "blob:https://www.youtube.com/123"):
            with self.subTest(url=url):
                self.assertIs(decide_embedded_frame_navigation(url), NavigationDecision.ALLOW)

    def test_blocks_insecure_and_local_frames(self) -> None:
        for url in ("http://ads.example.com", "file:///C:/secret.txt"):
            with self.subTest(url=url):
                self.assertIs(decide_embedded_frame_navigation(url), NavigationDecision.BLOCK)


if __name__ == "__main__":
    unittest.main()
