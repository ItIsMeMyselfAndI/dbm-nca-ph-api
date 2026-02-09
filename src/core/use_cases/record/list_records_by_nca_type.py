from core.interfaces.record_repository import RecordRepository


class ListRecordsByNCAType:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, nca_type: str, cursor: int, limit: int):
        return self.record_repository.list_records_by_nca_type(nca_type, cursor, limit)
