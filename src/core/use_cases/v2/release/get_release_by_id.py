from src.core.entities.release import Release
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_release_repository import AsyncReleaseRepository


class GetReleaseById:
    def __init__(self, release_repository: AsyncReleaseRepository):
        self.release_repository = release_repository

    async def execute(self, id: str) -> Release:
        release = await self.release_repository.get_release_by_id(id)
        if release is None:
            raise NotFoundError("Release", id)
        return release
