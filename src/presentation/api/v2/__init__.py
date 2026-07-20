from fastapi import APIRouter

from src.presentation.api.v2.routers.releases import router as releases_router
from src.presentation.api.v2.routers.records import router as records_router
from src.presentation.api.v2.routers.allocations import router as allocations_router
from src.presentation.api.v2.routers.pipeline import router as pipeline_router

router = APIRouter(prefix="/v2")

router.include_router(releases_router)
router.include_router(records_router)
router.include_router(allocations_router)
router.include_router(pipeline_router)
