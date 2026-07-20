import json
from pathlib import Path
from typing import Dict, List

from src.core.entities.allocation import Allocation
from src.core.entities.allocation_filter import AllocationFilter


class MockAsyncAllocationRepository:
    def __init__(self):
        self.allocations = self._get_mock_allocations()

    def _get_mock_allocations(self):
        base_path = Path(__file__).parent.parent
        json_path = base_path / "data" / "allocations.json"
        with open(json_path) as f:
            data = json.load(f)
        return [Allocation(**item) for item in data]

    async def get_allocation_by_id(self, id: str) -> Allocation | None:
        id = id.strip().lower()
        return next((a for a in self.allocations if a.id == id), None)

    async def list_allocations(self, limit: int, cursor: str | None = None) -> List[Allocation]:
        allocations = self.allocations
        if cursor:
            cursor = cursor.strip().lower()
            idx = next((i for i, a in enumerate(self.allocations) if a.id == cursor), None)
            if idx is None:
                return []
            allocations = self.allocations[idx + 1 :]
        return allocations[:limit]

    async def list_allocations_by_filter(
        self, limit: int, filter: Dict[AllocationFilter, str], cursor: str | None = None
    ) -> List[Allocation]:
        allocations = self.allocations
        if cursor:
            cursor = cursor.strip().lower()
            idx = next((i for i, a in enumerate(self.allocations) if a.id == cursor), None)
            if idx is None:
                return []
            allocations = self.allocations[idx + 1 :]
        key, value = list(filter.items())[0]
        allocations = [a for a in allocations if getattr(a, key.value) == value]
        return allocations[:limit]
