from src.core.entities.record_filter import RecordFilter
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.interfaces.async_record_repository import AsyncRecordRepository


class DeleteRecord:
    def __init__(
        self,
        record_repository: AsyncRecordRepository,
        allocation_repository: AsyncAllocationRepository,
    ):
        self.record_repository = record_repository
        self.allocation_repository = allocation_repository

    async def execute(self, nca_number: str) -> None:
        existing_records = await self.record_repository.list_records_by_filter(
            limit=1, filter={RecordFilter.NCA_NUMBER: nca_number}
        )
        if not existing_records:
            raise NotFoundError("Record", nca_number)

        record = existing_records[0]
        await self.record_repository.delete_record(record.id)
