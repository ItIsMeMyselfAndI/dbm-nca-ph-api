from src.core.entities.release import Release
from src.core.interfaces.async_release_repository import AsyncReleaseRepository


class UpsertRelease:
    def __init__(self, release_repository: AsyncReleaseRepository):
        self.release_repository = release_repository

    async def execute(self, release: Release) -> Release:
        existing = await self.release_repository.get_release_by_id(release.id)
        if existing is not None:
            return await self.release_repository.update_release(release.id, release)
        return await self.release_repository.create_release(release)
