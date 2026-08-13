from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .api.servers import router

app = FastAPI(title="Infrastructure Inventory API")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready"}

Instrumentator().instrument(app).expose(app)