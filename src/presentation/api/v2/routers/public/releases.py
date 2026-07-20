from fastapi import APIRouter, Depends, HTTPException

from src.core.exceptions import NotFoundError, ValidationError
from src.core.interfaces.async_release_repository import AsyncReleaseRepository
from src.core.use_cases.v2.release.get_release_by_id import GetReleaseById
from src.core.use_cases.v2.release.list_releases import ListReleases
from src.presentation.api.dependencies_v2 import get_release_repository
from src.presentation.api.schemas import CursorPageResponse, ReleaseResponse

router = APIRouter(prefix="/releases")


@router.get("", response_model=CursorPageResponse[ReleaseResponse])
async def list_releases(
    cursor: str | None = None,
    limit: int = 20,
    repo: AsyncReleaseRepository = Depends(get_release_repository),
):
    try:
        use_case = ListReleases(repo)
        releases, next_cursor = await use_case.execute(cursor=cursor, limit=limit)

        response = CursorPageResponse(
            items=releases,
            count=len(releases),
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


@router.get("/{id}", response_model=ReleaseResponse)
async def get_release_by_id(
    id: str,
    repo: AsyncReleaseRepository = Depends(get_release_repository),
):
    try:
        use_case = GetReleaseById(repo)
        release = await use_case.execute(id)
        return release

    except NotFoundError as ne:
        raise HTTPException(status_code=404, detail=str(ne))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
