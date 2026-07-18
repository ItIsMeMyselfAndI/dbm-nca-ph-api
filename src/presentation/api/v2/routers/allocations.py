from fastapi import APIRouter, Depends, HTTPException

from src.core.entities.allocation_filter import AllocationFilter
from src.core.exceptions import NotFoundError, ValidationError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.use_cases.v2.allocation.get_allocation_by_id import GetAllocationByID
from src.core.use_cases.v2.allocation.list_allocations import ListAllocations
from src.core.use_cases.v2.allocation.list_allocations_by_filter import (
    ListAllocationsByFilter,
)
from src.presentation.api.dependencies_v2 import get_allocation_repository
from src.presentation.api.schemas import AllocationResponse, CursorPageResponse

router = APIRouter(prefix="/allocations")


@router.get("", response_model=CursorPageResponse[AllocationResponse])
async def list_allocations(
    cursor: str | None = None,
    limit: int = 20,
    repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = ListAllocations(repo)
        allocations, next_cursor = await use_case.execute(cursor=cursor, limit=limit)

        response = CursorPageResponse(
            items=allocations,
            count=len(allocations),
            cursor=cursor,
            next_cursor=next_cursor,
        )
        return response

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=AllocationResponse)
async def get_allocation_by_id(
    id: str,
    repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = GetAllocationByID(repo)
        allocation = await use_case.execute(id)
        return allocation

    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{filter_key}/{filter_value}",
    response_model=CursorPageResponse[AllocationResponse],
)
async def list_allocations_by_filter(
    filter_key: AllocationFilter,
    filter_value: str,
    cursor: str | None = None,
    limit: int = 20,
    repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = ListAllocationsByFilter(repo)
        filter = {filter_key: filter_value}
        allocations, next_cursor = await use_case.execute(
            cursor=cursor, filter=filter, limit=limit
        )

        response = CursorPageResponse(
            items=allocations,
            count=len(allocations),
            cursor=cursor,
            next_cursor=next_cursor,
        )
        return response

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
