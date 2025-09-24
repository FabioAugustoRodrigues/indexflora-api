from app.models.schema_model import SearchSchemaModel
from app.validators.schema_validator import SchemaValidator
from app.infrastructure.redis.redis_search_client import RedisSearchClient

class DocumentService:
    def __init__(self, redisSearchService: RedisSearchClient):
        self.redisSearchService = redisSearchService

    def index_document(self, index_name: str, document_id: str, fields: dict):
        schema = SearchSchemaModel.get_by_redis_index_name(index_name)
        warning = None

        if schema:
            extra, missing = SchemaValidator.validate(fields, schema.fields)
            if extra or missing:
                warning = {"extra_fields": extra, "missing_fields": missing}
        else:
            warning = {"warning": f"Schema for index '{index_name}' not found."}

        index_name = self.redisSearchService.add_document(index_name, document_id, fields)

        return index_name

    def search_document(self, index_name: str, term: str, limit: int = 10, offset: int = 0):
        return self.redisSearchService.search_documents(index_name, term, limit, offset)