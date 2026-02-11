from typing import List, Tuple
from src.core.entities.release import Release
from src.core.interfaces.release_repository import ReleaseRepository


class ListReleases:
    def __init__(self, release_repository: ReleaseRepository):
        self.release_repository = release_repository

    def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Release], str | None]:
        releases = self.release_repository.list_releases(limit + 1, cursor)
        has_more = len(releases) == limit + 1

        next_cursor = releases[-1].id if has_more else None
        relevant_releases = releases[:limit]
        return relevant_releases, next_cursor
