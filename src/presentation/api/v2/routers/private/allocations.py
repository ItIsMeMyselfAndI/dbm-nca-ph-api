import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.entities.allocation import Allocation
from src.core.exceptions import NotFoundError
from src.core.interfaces.async_allocation_repository import AsyncAllocationRepository
from src.core.use_cases.v2.pipeline.delete_allocation import DeleteAllocation
from src.core.use_cases.v2.pipeline.upsert_allocation import UpsertAllocation
from src.presentation.api.dependencies_v2 import get_allocation_repository
from src.presentation.api.schemas import AllocationCreate

router = APIRouter(prefix="/allocations")


@router.post("", status_code=status.HTTP_201_CREATED)
async def upsert_allocation(
    data: AllocationCreate,
    allocation_repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = UpsertAllocation(allocation_repo)
        allocation = await use_case.execute(
            Allocation(id=str(uuid.uuid4()), **data.model_dump())
        )
        return allocation
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_allocation(
    id: str,
    allocation_repo: AsyncAllocationRepository = Depends(get_allocation_repository),
):
    try:
        use_case = DeleteAllocation(allocation_repo)
        await use_case.execute(id)
    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
