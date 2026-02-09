from typing import List, Protocol

from src.core.domain.allocation import Allocation


class AllocationRepository(Protocol):
    def get_allocation_by_id(self, id: int) -> Allocation:
        """Get an allocation by its ID."""
        ...

    def list_allocations(self, cursor: int, limit: int) -> List[Allocation]:
        """List all allocations with pagination."""
        ...

    def list_allocations_by_agency(
        self, agency_id: str, cursor: int, limit: int
    ) -> List[Allocation]:
        """List allocations filtered by agency ID with pagination."""
        ...

    def list_allocations_by_nca_number(
        self, nca_number: str, cursor: int, limit: int
    ) -> List[Allocation]:
        """List allocations filtered by NCA number with pagination."""
        ...

    def list_allocations_by_operating_unit(
        self, operating_unit: str, cursor: int, limit: int
    ) -> List[Allocation]:
        """List allocations filtered by operating unit ID with pagination."""
        ...
