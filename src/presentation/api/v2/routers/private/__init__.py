from fastapi import APIRouter, Depends

from src.presentation.api.auth import require_pipeline_key
from src.presentation.api.schemas import EndpointInfo, IndexResponse
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


@router.get("/", response_model=IndexResponse)
def private_index():
    return IndexResponse(
        title="DBM NCA PH API",
        version="v2/private",
        description="Authenticated write endpoints for automated data ingestion. All routes require X-API-Key header.",
        endpoints=[
            EndpointInfo(method="POST", path="/v2/private/releases", description="Upsert a release (by id)"),
            EndpointInfo(method="DELETE", path="/v2/private/releases/{id}", description="Delete a release and cascade records/allocations"),
            EndpointInfo(method="POST", path="/v2/private/records", description="Upsert a record (by nca_number)"),
            EndpointInfo(method="DELETE", path="/v2/private/records/{nca_number}", description="Delete a record and cascade allocations"),
            EndpointInfo(method="POST", path="/v2/private/allocations", description="Upsert an allocation (by composite key)"),
            EndpointInfo(method="DELETE", path="/v2/private/allocations/{id}", description="Delete an allocation"),
        ],
        docs_url="/docs",
    )
