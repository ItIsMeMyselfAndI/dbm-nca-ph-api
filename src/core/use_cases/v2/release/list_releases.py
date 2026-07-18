from typing import List, Tuple

from src.core.entities.release import Release
from src.core.exceptions import ValidationError
from src.core.interfaces.async_release_repository import AsyncReleaseRepository
from src.core.use_cases.v2._cursor import compute_next_cursor


class ListReleases:
    def __init__(self, release_repository: AsyncReleaseRepository):
        self.release_repository = release_repository

    async def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Release], str | None]:
        if limit <= 0:
            return [], None

        if cursor == "":
            raise ValidationError("Cursor cannot be an empty string.")

        releases = await self.release_repository.list_releases(limit, cursor)
        next_cursor = compute_next_cursor(releases)
        return releases, next_cursor
