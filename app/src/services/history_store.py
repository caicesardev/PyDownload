import json
from pathlib import Path

from src.models.history_entry import HistoryEntry

MAX_ENTRIES = 500


class HistoryStore:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._entries = self._load()

    @property
    def entries(self) -> tuple[HistoryEntry, ...]:
        return tuple(self._entries)

    def add(self, entry: HistoryEntry) -> None:
        self._entries.insert(0, entry)
        del self._entries[MAX_ENTRIES:]
        self._save()

    def remove(self, entry: HistoryEntry) -> None:
        if entry in self._entries:
            self._entries.remove(entry)
            self._save()

    def clear(self) -> None:
        self._entries.clear()
        self._save()

    def _load(self) -> list[HistoryEntry]:
        try:
            raw_entries = json.loads(self._file_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return []
        if not isinstance(raw_entries, list):
            return []
        return [HistoryEntry.from_dict(raw) for raw in raw_entries if isinstance(raw, dict)]

    def _save(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self._file_path.with_suffix(".tmp")
        serialized = json.dumps([entry.to_dict() for entry in self._entries], ensure_ascii=False, indent=2)
        temporary_path.write_text(serialized, encoding="utf-8")
        temporary_path.replace(self._file_path)
