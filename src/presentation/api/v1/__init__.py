from fastapi import APIRouter

from src.presentation.api.schemas import EndpointInfo, IndexResponse
from src.presentation.api.v1.routers.public.releases import router as releases_router
from src.presentation.api.v1.routers.public.records import router as records_router
from src.presentation.api.v1.routers.public.allocations import router as allocations_router

router = APIRouter(prefix="/v1")

router.include_router(releases_router)
router.include_router(records_router)
router.include_router(allocations_router)


@router.get("/", response_model=IndexResponse)
def v1_index():
    return IndexResponse(
        title="DBM NCA PH API",
        version="v1",
        description="Synchronous read-only endpoints backed by Supabase REST API",
        endpoints=[
            EndpointInfo(method="GET", path="/v1/releases", description="List releases (cursor pagination)"),
            EndpointInfo(method="GET", path="/v1/releases/{id}", description="Get release by ID"),
            EndpointInfo(method="GET", path="/v1/records", description="List records (cursor pagination)"),
            EndpointInfo(method="GET", path="/v1/records/{id}", description="Get record by ID"),
            EndpointInfo(method="GET", path="/v1/records/{filter_key}/{filter_value}", description="List records by filter"),
            EndpointInfo(method="GET", path="/v1/allocations", description="List allocations (cursor pagination)"),
            EndpointInfo(method="GET", path="/v1/allocations/{id}", description="Get allocation by ID"),
            EndpointInfo(method="GET", path="/v1/allocations/{filter_key}/{filter_value}", description="List allocations by filter"),
        ],
        docs_url="/docs",
    )
