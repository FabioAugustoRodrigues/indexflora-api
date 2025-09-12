from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from app.routes.schema_route import router as schema_route
from app.routes.document_route import router as document_route

from app.schemas.response import create_error_response

app = FastAPI(
    title="IndexFlora API",
    description="",
    version="0.1.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=create_error_response(
            message="Internal server error",
            errors=[str(exc)]
        ).dict(exclude_none=True)
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            message=exc.detail,
            errors=[exc.detail]
        ).dict(exclude_none=True)
    )

app.include_router(schema_route, prefix="/schemas", tags=["Schemas"])
app.include_router(document_route, prefix="/documents", tags=["Documents"])