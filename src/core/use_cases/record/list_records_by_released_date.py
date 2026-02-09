from src.core.interfaces.record_repository import RecordRepository


class ListRecordsByReleasedDate:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, released_date: str, cursor: int, limit: int):
        return self.record_repository.list_records_by_released_date(
            released_date, cursor, limit
        )
