from fastapi import APIRouter, Depends

from src.presentation.api.auth import require_pipeline_key
from src.presentation.api.v2.routers.private.releases import router as releases_router
from src.presentation.api.v2.routers.private.records import router as records_router
from src.presentation.api.v2.routers.private.allocations import router as allocations_router

router = APIRouter(
    prefix="/private",
    dependencies=[Depends(require_pipeline_key)],
)

router.include_router(releases_router)
router.include_router(records_router)
router.include_router(allocations_router)
