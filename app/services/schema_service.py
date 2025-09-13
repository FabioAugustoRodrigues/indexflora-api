from app.models.schema_model import SearchSchemaModel
from app.services.redis_search_service import RedisSearchService
from app.configs.settings import settings

import json

class SchemaService:
    def __init__(self):
        self.redis_search_service = RedisSearchService(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def create_schema(self, name: str, fields: list):
        schema = SearchSchemaModel(
            name=name,
            redis_index_name=f"idx:{name.lower()}",
            fields=json.dumps(fields)
        )

        schema.save()

        redis_result = self.redis_search_service.create_index(
            index_name=f"idx:{name.lower()}",
            fields=fields
        )

        return {
            "index_name": schema.redis_index_name,
            "redisearch": redis_result
        }
