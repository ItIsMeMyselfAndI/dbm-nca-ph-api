from fastapi import APIRouter, Depends, HTTPException

from src.core.interfaces.release_repository import ReleaseRepository

from src.core.use_cases.v1.release.get_release_by_id import GetReleaseById
from src.core.use_cases.v1.release.list_releases import ListReleases

from src.presentation.api.schemas import CursorPageResponse, ReleaseResponse
from src.presentation.api.dependencies import get_release_repository

router = APIRouter(prefix="/releases")


@router.get("", response_model=CursorPageResponse[ReleaseResponse])
def list_releases(
    cursor: str | None = None,
    limit: int = 20,
    repo: ReleaseRepository = Depends(get_release_repository),
):
    try:
        use_case = ListReleases(repo)
        releases, next_cursor = use_case.execute(cursor=cursor, limit=limit)

        response = CursorPageResponse(
            items=releases,
            count=len(releases),
            cursor=cursor,
            next_cursor=next_cursor,
        )
        return response

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=ReleaseResponse)
def get_release_by_id(
    id: str,
    repo: ReleaseRepository = Depends(get_release_repository),
):
    try:
        use_case = GetReleaseById(repo)
        release = use_case.execute(id)
        return release

    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
