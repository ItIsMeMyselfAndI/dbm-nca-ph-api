from src.core.interfaces.release_repository import ReleaseRepository


class GetReleaseById:
    def __init__(self, release_repository: ReleaseRepository):
        self.release_repository = release_repository

    def execute(self, id: str):
        return self.release_repository.get_release_by_id(id)
