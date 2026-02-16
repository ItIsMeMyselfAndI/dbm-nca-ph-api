from pathlib import Path
from typing import List
import json

from src.core.entities.release import Release
from src.core.interfaces.release_repository import ReleaseRepository


class MockReleaseRepository(ReleaseRepository):
    def __init__(self):
        self.releases = self._get_mock_releases()

    def _get_mock_releases(self):
        base_path = Path(__file__).parent.parent
        json_path = base_path / "data" / "releases.json"

        with open(json_path, "r") as f:
            data = json.load(f)
        return [Release(**item) for item in data]

    def get_release_by_id(self, id: str) -> Release:
        release = next((r for r in self.releases if r.id == id), None)
        if not release:
            raise ValueError(f"Release with ID {id} not found.")
        return release

    def list_releases(self, limit: int, cursor: str | None = None) -> List[Release]:
        releases = self.releases
        if cursor:
            try:
                cursor_index = next(i for i, r in enumerate(releases) if r.id == cursor)
                releases = releases[cursor_index + 1 :]
            except StopIteration:
                raise ValueError(f"Cursor with ID {cursor} not found.")

        releases = releases[:limit]
        return releases
