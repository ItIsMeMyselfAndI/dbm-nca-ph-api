import uvicorn
from fastapi import FastAPI

from src.presentation.api import v1

app = FastAPI(title="Philippine DBM NCA API")
app.include_router(v1.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "API is running", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
