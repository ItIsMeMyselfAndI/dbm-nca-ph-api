from typing import List, Protocol

from core.domain.release import Release


class ReleaseRepository(Protocol):
    def get_release_by_id(self, release_id: str) -> Release:
        """Get a release by its ID."""
        ...

    def list_releases(self, cursor: int, limit: int) -> List[Release]:
        """List all releases with pagination."""
        ...
