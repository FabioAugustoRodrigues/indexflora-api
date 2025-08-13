from fastapi import APIRouter, HTTPException

from app.schemas.schema import CreateSchemaRequest
from app.models.schema_model import SearchSchemaModel

import json

router = APIRouter()

@router.post("/")
def create_schema(req: CreateSchemaRequest):
    schema = SearchSchemaModel(
        name=req.name,
        redis_index_name=f"idx:{req.name.lower()}",
        fields=json.dumps([field.dict() for field in req.fields])
    )

    try:
        schema.save()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was an error: {e}")

    return {"message": "Schema created successfully", "index_name": schema.redis_index_name}
