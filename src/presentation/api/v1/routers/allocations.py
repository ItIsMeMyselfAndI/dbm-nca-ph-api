from fastapi import APIRouter, Depends

from src.core.domain.allocation_filter import AllocationFilter

from src.core.interfaces.allocation_repository import AllocationRepository

from src.core.use_cases.allocation.get_allocation_by_id import GetAllocationByID
from src.core.use_cases.allocation.list_allocations import ListAllocations
from src.core.use_cases.allocation.list_allocations_by_filter import (
    ListAllocationsByFilter,
)

from src.presentation.api.schemas import AllocationResponse, CursorPageResponse
from src.presentation.api.dependencies import get_allocation_repository

router = APIRouter(prefix="/allocations")


@router.get("", response_model=CursorPageResponse[AllocationResponse])
def list_allocations(
    cursor: str | None = None,
    limit: int = 20,
    repo: AllocationRepository = Depends(get_allocation_repository),
):
    use_case = ListAllocations(repo)
    allocations, next_cursor = use_case.execute(cursor=cursor, limit=limit)

    response = CursorPageResponse(
        items=allocations,
        cursor=cursor,
        next_cursor=next_cursor,
    )
    return response


@router.get("/{id}", response_model=AllocationResponse)
def get_allocation_by_id(
    id: str,
    repo: AllocationRepository = Depends(get_allocation_repository),
):
    use_case = GetAllocationByID(repo)
    allocation = use_case.execute(id)
    return allocation


@router.get(
    "/{filter_key}/{filter_value}",
    response_model=CursorPageResponse[AllocationResponse],
)
def list_allocations_by_filter(
    filter_key: AllocationFilter,
    filter_value: str,
    cursor: str | None = None,
    limit: int = 20,
    repo: AllocationRepository = Depends(get_allocation_repository),
):
    use_case = ListAllocationsByFilter(repo)

    filter = {filter_key: filter_value}
    allocations, next_cursor = use_case.execute(
        cursor=cursor, filter=filter, limit=limit
    )

    response = CursorPageResponse(
        items=allocations,
        cursor=cursor,
        next_cursor=next_cursor,
    )
    return response
