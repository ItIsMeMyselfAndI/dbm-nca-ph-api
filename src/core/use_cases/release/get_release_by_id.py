from src.core.entities.release import Release
from src.core.interfaces.release_repository import ReleaseRepository


class GetReleaseById:
    def __init__(self, release_repository: ReleaseRepository):
        self.release_repository = release_repository

    def execute(self, id: str) -> Release:
        try:
            release = self.release_repository.get_release_by_id(id)
            if release is None:
                raise ValueError(f"Release with ID {id} not found.")
            return release

        except ValueError as e:
            raise ValueError(f"Release with ID {id} not found.") from e
