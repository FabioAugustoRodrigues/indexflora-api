from app.models.schema_model import SearchSchemaModel
from app.services.redis_search_service import RedisSearchService

import json

class SchemaService:
    def __init__(self, redis_host="redis", redis_port=6379):
        self.redis_service = RedisSearchService(host=redis_host, port=redis_port)

    def create_schema(self, name: str, fields: list):
        schema = SearchSchemaModel(
            name=name,
            redis_index_name=f"idx:{name.lower()}",
            fields=json.dumps(fields)
        )

        schema.save()

        redis_result = self.redis_service.create_index(
            index_name=f"idx:{name.lower()}",
            fields=fields
        )

        return {
            "index_name": schema.redis_index_name,
            "redisearch": redis_result
        }
