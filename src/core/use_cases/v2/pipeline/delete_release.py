from src.core.entities.record_filter import RecordFilter
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.interfaces.async_record_repository import AsyncRecordRepository
from src.core.interfaces.async_release_repository import AsyncReleaseRepository


class DeleteRelease:
    def __init__(
        self,
        release_repository: AsyncReleaseRepository,
        record_repository: AsyncRecordRepository,
        allocation_repository: AsyncAllocationRepository,
    ):
        self.release_repository = release_repository
        self.record_repository = record_repository
        self.allocation_repository = allocation_repository

    async def execute(self, id: str) -> None:
        release = await self.release_repository.get_release_by_id(id)
        if release is None:
            raise NotFoundError("Release", id)

        records = await self.record_repository.list_records_by_filter(
            limit=10000, filter={RecordFilter.RELEASE_ID: id}
        )

        for record in records:
            await self.record_repository.delete_record(record.id)

        await self.release_repository.delete_release(id)
