from fastapi import FastAPI
from app.routes.schema_route import router as schema_route
from app.routes.document_route import router as document_route

app = FastAPI(
    title="IndexFlora API",
    description="",
    version="0.1.0"
)

app.include_router(schema_route, prefix="/schemas", tags=["Schemas"])
app.include_router(document_route, prefix="/documents", tags=["Documents"])