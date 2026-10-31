from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HistoryEntry:
    title: str
    url: str
    summary: str
    filepath: str
    completed_at: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "HistoryEntry":
        return cls(
            title=str(raw.get("title", "")),
            url=str(raw.get("url", "")),
            summary=str(raw.get("summary", "")),
            filepath=str(raw.get("filepath", "")),
            completed_at=str(raw.get("completed_at", "")),
        )
