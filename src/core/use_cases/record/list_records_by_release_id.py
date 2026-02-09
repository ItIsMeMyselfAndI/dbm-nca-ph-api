from src.core.interfaces.record_repository import RecordRepository


class ListRecordsByReleaseId:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, release_id: str, cursor: int, limit: int):
        return self.record_repository.list_records_by_release_id(
            release_id, cursor, limit
        )
