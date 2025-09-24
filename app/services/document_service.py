from app.models.schema_model import SearchSchemaModel
from app.validators.schema_validator import SchemaValidator
from app.infrastructure.redis.redis_search_client import RedisSearchClient
from app.configs.settings import settings
from fastapi import HTTPException

class DocumentService:
    def __init__(self):
        self.redis_client = RedisSearchClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def index_document(self, index_name: str, document_id: str, fields: dict):
        self.check_for_fields_in_schema(index_name, fields)
        
        return self.redis_client.add_document(index_name, document_id, fields)

    def search_documents(self, index_name: str, term: str, limit: int = 10, offset: int = 0):
        return self.redis_client.search_documents(index_name, term, limit, offset)

    def check_for_fields_in_schema(self, index_name: str, fields: dict):
        schema = SearchSchemaModel.get_by_redis_index_name(index_name)

        if not schema:
            raise HTTPException(status_code=404, detail=f"Schema for index '{index_name}' not found.")
        
        extra, missing = SchemaValidator.validate(fields, schema.fields)

        if extra:
            extra_fields = ", ".join(extra)
            raise HTTPException(status_code=400, detail=f"There are extra fields in the document that are not in the schema for index '{index_name}': {extra_fields}.")

        if missing:
            missing_fields = ", ".join(missing)
            raise HTTPException(status_code=400, detail=f"There are missing fields in the document that are in the schema for index '{index_name}': {missing_fields}.")