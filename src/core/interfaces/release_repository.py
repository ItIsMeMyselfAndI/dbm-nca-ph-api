from typing import List, Protocol

from src.core.domain.release import Release


class ReleaseRepository(Protocol):
    def get_release_by_id(self, id: str) -> Release:
        """Get a release by its ID."""
        ...

    def list_releases(self, limit: int, cursor: str | None = None) -> List[Release]:
        """List all releases with pagination."""
        ...
