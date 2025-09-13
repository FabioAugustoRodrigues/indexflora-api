from fastapi import APIRouter, HTTPException

from app.schemas.schema import CreateSchemaRequest
from app.schemas.response import create_success_response, create_error_response
from app.models.schema_model import SearchSchemaModel
from app.services.redis_search_service import RedisSearchService

import json

router = APIRouter()
redisSearchService = RedisSearchService(host="redis", port=6379)

@router.post("/")
def create_schema(req: CreateSchemaRequest):
    schema = SearchSchemaModel(
        name=req.name,
        redis_index_name=f"idx:{req.name.lower()}",
        fields=json.dumps([field.dict() for field in req.fields])
    )

    schema.save()

    redis_result = redisSearchService.create_index(
        index_name=f"idx:{req.name.lower()}",
        fields=[field.dict() for field in req.fields]
    )

    response_data = {
        "index_name": schema.redis_index_name,
        "redisearch": redis_result
    }
        
    return create_success_response(
        data=response_data,
        message="Schema created successfully and index created in Redisearch"
    )