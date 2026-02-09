from src.core.interfaces.release_repository import ReleaseRepository


class ListReleases:
    def __init__(self, release_repository: ReleaseRepository):
        self.release_repository = release_repository

    def execute(self, cursor: int, limit: int):
        return self.release_repository.list_releases(cursor, limit)
