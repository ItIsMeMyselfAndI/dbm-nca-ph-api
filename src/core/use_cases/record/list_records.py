from core.interfaces.record_repository import RecordRepository


class ListRecords:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, cursor: int, limit: int):
        return self.record_repository.list_records(cursor, limit)
