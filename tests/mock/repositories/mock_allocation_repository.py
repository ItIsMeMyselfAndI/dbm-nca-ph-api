import json
from pathlib import Path
from typing import Dict, List

from src.core.entities.allocation_filter import AllocationFilter
from src.core.entities.allocation import Allocation
from src.core.interfaces.allocation_repository import AllocationRepository


class MockAllocationRepository(AllocationRepository):
    def __init__(self):
        self.allocations = self._get_mock_allocations()

    def _get_mock_allocations(self):
        base_path = Path(__file__).parent.parent
        json_path = base_path / "data" / "allocations.json"

        with open(json_path, "r") as f:
            data = json.load(f)
        return [Allocation(**item) for item in data]

    def get_allocation_by_id(self, id: str) -> Allocation:
        id = id.strip().lower()
        allocation = next((a for a in self.allocations if a.id == id), None)
        if not allocation:
            raise ValueError(f"Allocation with ID {id} not found.")
        return allocation

    def list_allocations(
        self, limit: int, cursor: str | None = None
    ) -> List[Allocation]:
        allocations = self.allocations
        if cursor:
            cursor = cursor.strip().lower()
            try:
                cursor_index = next(
                    i for i, a in enumerate(self.allocations) if a.id == cursor
                )
                allocations = self.allocations[cursor_index + 1 :]
            except StopIteration:
                raise ValueError(f"Cursor with ID {cursor} not found.")

        allocations = allocations[:limit]
        return allocations

    def list_allocations_by_filter(
        self, limit: int, filter: Dict[AllocationFilter, str], cursor: str | None = None
    ) -> List[Allocation]:
        allocations = self.allocations
        if cursor:
            cursor = cursor.strip().lower()
            try:
                cursor_index = next(
                    i for i, a in enumerate(self.allocations) if a.id == cursor
                )
                allocations = self.allocations[cursor_index + 1 :]
            except StopIteration:
                raise ValueError(f"Cursor with ID {cursor} not found.")

        key, value = list(filter.items())[0]
        allocations = [a for a in allocations if getattr(a, key.value) == value]
        allocations = allocations[:limit]
        return allocations
