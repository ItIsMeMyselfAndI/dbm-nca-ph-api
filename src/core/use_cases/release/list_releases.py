from typing import List, Tuple
from src.core.entities.release import Release
from src.core.interfaces.release_repository import ReleaseRepository


class ListReleases:
    def __init__(self, release_repository: ReleaseRepository):
        self.release_repository = release_repository

    def execute(
        self, limit: int, cursor: str | None = None
    ) -> Tuple[List[Release], str | None]:
        if limit <= 0:
            return [], None

        releases = self.release_repository.list_releases(limit, cursor)
        if len(releases) < limit:
            next_cursor = None
        else:
            next_cursor = releases[-1].id
        return releases, next_cursor
