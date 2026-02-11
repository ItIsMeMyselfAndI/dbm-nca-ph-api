from src.core.entities.record import Record
from src.core.interfaces.record_repository import RecordRepository


class GetRecordByID:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, id: str) -> Record:
        """Get a record by its ID."""
        return self.record_repository.get_record_by_id(id)
