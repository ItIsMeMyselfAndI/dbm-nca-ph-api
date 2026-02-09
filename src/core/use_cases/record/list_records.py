from typing import Dict
from src.core.interfaces.record_repository import RecordRepository


class ListRecords:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, cursor: int, limit: int, filter: Dict[str, str] | None = None):
        if not filter:
            return self.record_repository.list_records(cursor, limit)

        key, value = next(iter(filter.items()))

        if key == "department":
            return self.record_repository.list_records_by_department(
                value, cursor, limit
            )
        elif key == "nca_type":
            return self.record_repository.list_records_by_nca_type(value, cursor, limit)
        elif key == "release_id":
            return self.record_repository.list_records_by_release_id(
                value, cursor, limit
            )
        elif key == "released_date":
            return self.record_repository.list_records_by_released_date(
                value, cursor, limit
            )
        else:
            raise ValueError(f"Unsupported filter key: {key}")
