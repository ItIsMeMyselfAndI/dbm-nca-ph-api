from src.core.interfaces.record_repository import RecordRepository


class ListRecordsByDepartment:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, department: str, cursor: int, limit: int):
        return self.record_repository.list_records_by_department(
            department, cursor, limit
        )
