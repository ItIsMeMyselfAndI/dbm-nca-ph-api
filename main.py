from slowapi.errors import RateLimitExceeded
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.presentation.api import v1
from src.presentation.api import v2
from src.presentation.api.schemas import EndpointInfo, IndexResponse

app = FastAPI(title="Philippine DBM NCA API")
app.include_router(v1.router)
app.include_router(v2.router)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = Limiter(key_func=get_remote_address, default_limits=["1000/hour"])
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler  # pyright: ignore
)


@app.get("/", response_model=IndexResponse)
def root():
    return IndexResponse(
        title="DBM NCA PH API",
        version="root",
        description="Philippine Department of Budget and Management (DBM) Notice of Cash Allocation (NCA) API. Provides access to DBM release, record, and allocation data via two backend versions.",
        endpoints=[
            EndpointInfo(method="GET", path="/v1/", description="v1 synchronous API index (Supabase backend)"),
            EndpointInfo(method="GET", path="/v2/", description="v2 asynchronous API index (PostgreSQL backend)"),
            EndpointInfo(method="GET", path="/v1/releases", description="List releases via v1"),
            EndpointInfo(method="GET", path="/v2/releases", description="List releases via v2"),
            EndpointInfo(method="GET", path="/v1/records", description="List records via v1"),
            EndpointInfo(method="GET", path="/v2/records", description="List records via v2"),
        ],
        docs_url="/docs",
    )


if __name__ == "__main__":
    import os
    import socket

    def _get_local_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "0.0.0.0"
        finally:
            s.close()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
