from fastapi import APIRouter

from app.schemas.schema import CreateSchemaRequest
from app.schemas.response import create_success_response, create_error_response
from app.services.schema_service import SchemaService

router = APIRouter()
schema_service = SchemaService(redis_host="redis", redis_port=6379)

@router.post("/")
def create_schema(req: CreateSchemaRequest):
    response_data = schema_service.create_schema(
        name=req.name,
        fields=[field.dict() for field in req.fields]
    )

    return create_success_response(
        data=response_data,
        message="Schema created successfully and index created in Redisearch"
    )
