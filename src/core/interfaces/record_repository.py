from typing import Dict, List, Protocol

from src.core.domain.record_filter import RecordFilter
from src.core.domain.record import Record


class RecordRepository(Protocol):
    def get_record_by_id(self, id: str) -> Record:
        """Get a record by its ID."""
        ...

    def get_record_by_nca_number(self, nca_number: str) -> Record:
        """Get a record by its NCA number."""
        ...

    def list_records(self, limit: int, cursor: str | None = None) -> List[Record]:
        """List all records with pagination."""
        ...

    def list_records_by_filter(
        self, limit: int, filter: Dict[RecordFilter, str], cursor: str | None = None
    ) -> List[Record]:
        """List filtered records with pagination."""
        ...
