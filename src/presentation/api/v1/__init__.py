from fastapi import APIRouter

from src.presentation.api.v1.routers.releases import router as releases_router
from src.presentation.api.v1.routers.records import router as records_router
from src.presentation.api.v1.routers.allocations import router as allocations_router

router = APIRouter(prefix="/v1")

router.include_router(releases_router)
router.include_router(records_router)
router.include_router(allocations_router)
