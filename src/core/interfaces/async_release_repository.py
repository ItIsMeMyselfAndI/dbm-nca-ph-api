from typing import List, Protocol

from src.core.entities.release import Release


class AsyncReleaseRepository(Protocol):
    async def get_release_by_id(self, id: str) -> Release | None: ...

    async def list_releases(
        self, limit: int, cursor: str | None = None
    ) -> List[Release]: ...

    async def create_release(self, release: Release) -> Release: ...

    async def update_release(self, id: str, release: Release) -> Release | None: ...

    async def delete_release(self, id: str) -> bool: ...
