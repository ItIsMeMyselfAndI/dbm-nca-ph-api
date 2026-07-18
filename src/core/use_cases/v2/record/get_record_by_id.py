from src.core.entities.record import Record
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_record_repository import AsyncRecordRepository


class GetRecordByID:
    def __init__(self, record_repository: AsyncRecordRepository):
        self.record_repository = record_repository

    async def execute(self, id: str) -> Record:
        record = await self.record_repository.get_record_by_id(id)
        if record is None:
            raise NotFoundError("Record", id)
        return record
