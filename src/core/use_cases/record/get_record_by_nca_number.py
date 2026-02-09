from core.interfaces.record_repository import RecordRepository


class GetRecordByNcaNumber:
    def __init__(self, record_repository: RecordRepository):
        self.record_repository = record_repository

    def execute(self, nca_number: str):
        return self.record_repository.get_record_by_nca_number(nca_number)
