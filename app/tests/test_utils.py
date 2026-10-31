import unittest

from src.utils.formatting import (
    format_bytes,
    format_count,
    format_duration,
    format_upload_date,
    friendly_codec_name,
)


class FormattingTest(unittest.TestCase):
    def test_formats_bytes_with_binary_units(self) -> None:
        self.assertEqual(format_bytes(512), "512 B")
        self.assertEqual(format_bytes(1536), "1.5 KB")
        self.assertEqual(format_bytes(18816948), "17.9 MB")

    def test_formats_durations(self) -> None:
        self.assertEqual(format_duration(58), "0:58")
        self.assertEqual(format_duration(3725), "1:02:05")

    def test_formats_counts(self) -> None:
        self.assertEqual(format_count(950), "950")
        self.assertEqual(format_count(12_000), "12 mil")
        self.assertEqual(format_count(1_534_200), "1.5 M")
        self.assertEqual(format_count(2_000_000_000), "2 mil M")

    def test_formats_upload_dates(self) -> None:
        self.assertEqual(format_upload_date("20140116"), "16/01/2014")
        self.assertEqual(format_upload_date(""), "")
        self.assertEqual(format_upload_date("2014-01"), "")

    def test_translates_codec_identifiers(self) -> None:
        self.assertEqual(friendly_codec_name("avc1.640028"), "H.264")
        self.assertEqual(friendly_codec_name("av01.0.08M.08"), "AV1")
        self.assertEqual(friendly_codec_name("theora"), "THEORA")


if __name__ == "__main__":
    unittest.main()
