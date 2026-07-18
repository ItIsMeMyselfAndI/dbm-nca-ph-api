from src.core.entities.record import Record
from src.core.interfaces.record_repository import RecordRepository


class GetRecordByID:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, id: str) -> Record:
        try:
            record = self.record_repository.get_record_by_id(id)
            if record is None:
                raise ValueError(f"Record with ID {id} not found.")
            return record

        except ValueError as e:
            raise ValueError(f"Record with ID {id} not found.") from e
