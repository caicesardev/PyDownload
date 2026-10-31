import tempfile
import unittest
from pathlib import Path

from src.models.history_entry import HistoryEntry
from src.services.history_store import MAX_ENTRIES, HistoryStore

ENTRY = HistoryEntry(
    title="Fox Snow Dive",
    url="https://www.youtube.com/watch?v=dP15zlyra3c",
    summary="Audio · 126 kbps · WEBM · Opus → MP3",
    filepath="C:/Downloads/Fox Snow Dive.mp3",
    completed_at="2026-10-31T18:00:00",
)


class HistoryStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.file_path = Path(self._temp.name) / "history.json"

    def tearDown(self) -> None:
        self._temp.cleanup()

    def test_persists_entries_newest_first(self) -> None:
        store = HistoryStore(self.file_path)
        older = HistoryEntry(**{**ENTRY.to_dict(), "title": "Older"})
        store.add(older)
        store.add(ENTRY)
        self.assertEqual(HistoryStore(self.file_path).entries, (ENTRY, older))

    def test_removes_and_clears_entries(self) -> None:
        store = HistoryStore(self.file_path)
        store.add(ENTRY)
        store.remove(ENTRY)
        self.assertEqual(HistoryStore(self.file_path).entries, ())
        store.add(ENTRY)
        store.clear()
        self.assertEqual(HistoryStore(self.file_path).entries, ())

    def test_caps_the_number_of_entries(self) -> None:
        store = HistoryStore(self.file_path)
        for index in range(MAX_ENTRIES + 5):
            store.add(HistoryEntry(**{**ENTRY.to_dict(), "title": str(index)}))
        self.assertEqual(len(store.entries), MAX_ENTRIES)
        self.assertEqual(store.entries[0].title, str(MAX_ENTRIES + 4))

    def test_ignores_corrupted_files(self) -> None:
        self.file_path.write_text("{not json", encoding="utf-8")
        self.assertEqual(HistoryStore(self.file_path).entries, ())
        self.file_path.write_text('{"title": "not a list"}', encoding="utf-8")
        self.assertEqual(HistoryStore(self.file_path).entries, ())


if __name__ == "__main__":
    unittest.main()
