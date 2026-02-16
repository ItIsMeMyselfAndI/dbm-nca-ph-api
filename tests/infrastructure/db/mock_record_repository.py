import json
from pathlib import Path
from typing import Dict, List

from src.core.entities.record_filter import RecordFilter
from src.core.entities.record import Record
from src.core.interfaces.record_repository import RecordRepository


class MockRecordRepository(RecordRepository):
    def __init__(self):
        self.records = self._get_mock_records()

    def _get_mock_records(self):
        base_path = Path(__file__).parent.parent.parent
        json_path = base_path / "mock_data" / "records.json"

        with open(json_path, "r") as f:
            data = json.load(f)
        return [Record(**item) for item in data]

    def get_record_by_id(self, id: str) -> Record:
        record = next((r for r in self.records if r.id == id), None)
        if not record:
            raise ValueError(f"Record with ID {id} not found.")
        return record

    def get_record_by_nca_number(self, nca_number: str) -> Record:
        record = next((r for r in self.records if r.nca_number == nca_number), None)
        if not record:
            raise ValueError(f"Record with NCA number {nca_number} not found.")
        return record

    def list_records(self, limit: int, cursor: str | None = None) -> List[Record]:
        records = self.records
        if cursor:
            try:
                cursor_index = next(i for i, r in enumerate(records) if r.id == cursor)
                records = records[cursor_index + 1 :]
            except StopIteration:
                raise ValueError(f"Cursor with ID {cursor} not found.")

        records = records[:limit]
        return records

    def list_records_by_filter(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> List[Record]:
        key, value = list(filter.items())[0]
        records = [r for r in self.records if getattr(r, key.value) == value]

        if cursor:
            try:
                cursor_index = next(i for i, r in enumerate(records) if r.id == cursor)
                records = records[cursor_index + 1 :]
            except StopIteration:
                raise ValueError(f"Cursor with ID {cursor} not found.")

        records = records[:limit]
        return records
