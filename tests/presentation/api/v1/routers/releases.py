from fastapi import APIRouter, Depends

from src.core.interfaces.release_repository import ReleaseRepository

from src.core.use_cases.release.get_release_by_id import GetReleaseById
from src.core.use_cases.release.list_releases import ListReleases

from src.presentation.api.schemas import CursorPageResponse, ReleaseResponse
from src.presentation.api.dependencies import get_release_repository

router = APIRouter(prefix="/releases")


@router.get("", response_model=CursorPageResponse[ReleaseResponse])
def list_releases(
    cursor: str | None = None,
    limit: int = 20,
    repo: ReleaseRepository = Depends(get_release_repository),
):
    use_case = ListReleases(repo)
    releases, next_cursor = use_case.execute(cursor=cursor, limit=limit)

    response = CursorPageResponse(
        items=releases,
        count=len(releases),
        cursor=cursor,
        next_cursor=next_cursor,
    )
    return response


@router.get("/{id}", response_model=ReleaseResponse)
def get_release_by_id(
    id: str,
    repo: ReleaseRepository = Depends(get_release_repository),
):
    use_case = GetReleaseById(repo)
    release = use_case.execute(id)
    return release
