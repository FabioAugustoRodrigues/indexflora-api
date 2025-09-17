from app.models.schema_model import SearchSchemaModel
from app.infrastructure.redis.redis_search_client import RedisSearchClient
from app.configs.settings import settings
from fastapi import HTTPException

import json

class SchemaService:
    def __init__(self):
        self.redis_client = RedisSearchClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def create_schema(self, name: str, fields: list):
        existing_schema = SearchSchemaModel.get_by_name(name)
        if existing_schema:
            raise HTTPException(status_code=409, detail="Index name is already in use.")

        schema = SearchSchemaModel(
            name=name,
            redis_index_name=f"idx:{name.lower()}",
            fields=json.dumps(fields)
        )

        schema.save()

        self.redis_client.create_index(
            index_name=f"idx:{name.lower()}",
            fields=fields
        )

        return schema.redis_index_name