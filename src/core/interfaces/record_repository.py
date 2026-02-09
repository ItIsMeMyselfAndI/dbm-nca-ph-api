from typing import List, Protocol

from core.domain.record import Record


class RecordRepository(Protocol):
    def get_record_by_id(self, record_id: str) -> Record:
        """Get a record by its ID."""
        ...

    def get_record_by_nca_number(self, nca_number: str) -> Record:
        """Get a record by its NCA number."""
        ...

    def list_records(self, cursor: int, limit: int) -> List[Record]:
        """List all records with pagination."""
        ...

    def list_records_by_department(
        self, department_id: str, cursor: int, limit: int
    ) -> List[Record]:
        """List records filtered by department ID with pagination."""
        ...

    def list_records_by_nca_type(
        self, nca_type: str, cursor: int, limit: int
    ) -> List[Record]:
        """List records filtered by NCA type with pagination."""
        ...

    def list_records_by_release_id(
        self, release_id: str, cursor: int, limit: int
    ) -> List[Record]:
        """List records filtered by release ID with pagination."""
        ...

    def list_records_by_released_date(
        self, released_date: str, cursor: int, limit: int
    ) -> List[Record]:
        """List records filtered by released date with pagination."""
        ...
