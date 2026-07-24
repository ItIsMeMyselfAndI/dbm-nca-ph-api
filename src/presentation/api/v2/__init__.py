from fastapi import APIRouter

from src.presentation.api.schemas import EndpointInfo, IndexResponse
from src.presentation.api.v2.routers.public.releases import router as releases_router
from src.presentation.api.v2.routers.public.records import router as records_router
from src.presentation.api.v2.routers.public.allocations import router as allocations_router
from src.presentation.api.v2.routers.private import router as private_router

router = APIRouter(prefix="/v2")

router.include_router(releases_router)
router.include_router(records_router)
router.include_router(allocations_router)
router.include_router(private_router)


@router.get("/", response_model=IndexResponse)
def v2_index():
    return IndexResponse(
        title="DBM NCA PH API",
        version="v2",
        description="Asynchronous API backed by PostgreSQL. Public read endpoints are open; private write endpoints under /v2/private/ require X-API-Key authentication.",
        endpoints=[
            EndpointInfo(method="GET", path="/v2/releases", description="List releases (cursor pagination)"),
            EndpointInfo(method="GET", path="/v2/releases/{id}", description="Get release by ID"),
            EndpointInfo(method="GET", path="/v2/records", description="List records (cursor pagination)"),
            EndpointInfo(method="GET", path="/v2/records/{id}", description="Get record by ID"),
            EndpointInfo(method="GET", path="/v2/records/{filter_key}/{filter_value}", description="List records by filter"),
            EndpointInfo(method="GET", path="/v2/allocations", description="List allocations (cursor pagination)"),
            EndpointInfo(method="GET", path="/v2/allocations/{id}", description="Get allocation by ID"),
            EndpointInfo(method="GET", path="/v2/allocations/{filter_key}/{filter_value}", description="List allocations by filter"),
            EndpointInfo(method="POST", path="/v2/private/releases", description="Upsert a release (auth required)"),
            EndpointInfo(method="DELETE", path="/v2/private/releases/{id}", description="Delete a release (auth required)"),
            EndpointInfo(method="POST", path="/v2/private/records", description="Upsert a record (auth required)"),
            EndpointInfo(method="DELETE", path="/v2/private/records/{nca_number}", description="Delete a record (auth required)"),
            EndpointInfo(method="POST", path="/v2/private/allocations", description="Upsert an allocation (auth required)"),
            EndpointInfo(method="DELETE", path="/v2/private/allocations/{id}", description="Delete an allocation (auth required)"),
        ],
        docs_url="/docs",
    )
