from fastapi import APIRouter, HTTPException

from app.schemas.schema import CreateSchemaRequest
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

    try:
        schema.save()

        redis_result = redisSearchService.create_index(
            index_name=f"idx:{req.name.lower()}",
            fields=[field.dict() for field in req.fields]
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was an error: {e}")

    return {
        "message": "Schema created successfully and index created in Redisearch",
        "index_name": schema.redis_index_name,
        "redisearch": redis_result
    }
