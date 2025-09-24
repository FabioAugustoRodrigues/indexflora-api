from app.models.schema_model import SearchSchemaModel
from app.validators.schema_validator import SchemaValidator
from app.infrastructure.redis.redis_search_client import RedisSearchClient
from app.configs.settings import settings

class DocumentService:
    def __init__(self):
        self.redis_client = RedisSearchClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def index_document(self, index_name: str, document_id: str, fields: dict):
        schema = SearchSchemaModel.get_by_redis_index_name(index_name)
        warning = None

        if schema:
            extra, missing = SchemaValidator.validate(fields, schema.fields)
            if extra or missing:
                warning = {"extra_fields": extra, "missing_fields": missing}
        else:
            warning = {"warning": f"Schema for index '{index_name}' not found."}

        index_name = self.redis_client.add_document(index_name, document_id, fields)

        return index_name

    def search_documents(self, index_name: str, term: str, limit: int = 10, offset: int = 0):
        return self.redis_client.search_documents(index_name, term, limit, offset)