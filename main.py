from slowapi.errors import RateLimitExceeded
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.presentation.api import v1

app = FastAPI(title="Philippine DBM NCA API")
app.include_router(v1.router, prefix="/api")

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


@app.get("/")
def root():
    return {"message": "API is running", "docs": "/docs"}


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
