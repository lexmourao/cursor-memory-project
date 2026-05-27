"""Memory-bank loading service."""

from pathlib import Path

from app.models.memory import MemoryRecord


ALLOWED_MEMORY_FILES = {
    "README.md",
    "projectbrief.md",
    "productContext.md",
    "activeContext.md",
    "systemPatterns.md",
    "techContext.md",
    "progress.md",
}


class MemoryService:
    """Load memory-bank markdown files as structured records."""

    def __init__(self, memory_bank_dir: Path) -> None:
        self.memory_bank_dir = memory_bank_dir

    def memory_bank_exists(self) -> bool:
        """Return whether the configured memory-bank directory exists."""
        return self.memory_bank_dir.exists() and self.memory_bank_dir.is_dir()

    def list_records(self) -> list[MemoryRecord]:
        """Return allowed markdown files from memory-bank as memory records."""
        if not self.memory_bank_exists():
            return []

        records: list[MemoryRecord] = []

        for path in sorted(self.memory_bank_dir.glob("*.md")):
            if path.name not in ALLOWED_MEMORY_FILES:
                continue

            records.append(
                MemoryRecord(
                    id=path.stem,
                    source=str(path),
                    type="markdown",
                    content=path.read_text(encoding="utf-8"),
                )
            )

        return records

    def get_record(self, record_id: str) -> MemoryRecord | None:
        """Return one memory record by ID, if it exists."""
        for record in self.list_records():
            if record.id == record_id:
                return record

        return None
