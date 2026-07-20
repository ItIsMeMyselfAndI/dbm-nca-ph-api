import json
from pathlib import Path
from typing import List

from src.core.entities.release import Release


class MockAsyncReleaseRepository:
    def __init__(self):
        self.releases = self._get_mock_releases()

    def _get_mock_releases(self):
        base_path = Path(__file__).parent.parent
        json_path = base_path / "data" / "releases.json"
        with open(json_path) as f:
            data = json.load(f)
        return [Release(**item) for item in data]

    async def get_release_by_id(self, id: str) -> Release | None:
        id = id.strip().lower()
        return next((r for r in self.releases if r.id == id), None)

    async def list_releases(self, limit: int, cursor: str | None = None) -> List[Release]:
        releases = self.releases
        if cursor:
            cursor = cursor.strip().lower()
            idx = next((i for i, r in enumerate(self.releases) if r.id == cursor), None)
            if idx is None:
                return []
            releases = self.releases[idx + 1 :]
        return releases[:limit]

    async def create_release(self, release: Release) -> Release:
        self.releases.append(release)
        return release

    async def update_release(self, id: str, release: Release) -> Release | None:
        for i, r in enumerate(self.releases):
            if r.id == id:
                self.releases[i] = release
                return release
        return None

    async def delete_release(self, id: str) -> bool:
        for i, r in enumerate(self.releases):
            if r.id == id:
                self.releases.pop(i)
                return True
        return False
