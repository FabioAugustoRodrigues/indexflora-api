from app.models.schema_model import SearchSchemaModel
from app.services.schema_validator_service import SchemaValidatorService
from app.services.redis_search_service import RedisSearchService

class DocumentIndexerService:
    def __init__(self, redisSearchService: RedisSearchService):
        self.redisSearchService = redisSearchService

    def index_document(self, index_name: str, document_id: str, fields: dict):
        schema = SearchSchemaModel.get_by_redis_index_name(index_name)
        warning = None

        if schema:
            extra, missing = SchemaValidatorService.validate(fields, schema.fields)
            if extra or missing:
                warning = {"extra_fields": extra, "missing_fields": missing}
        else:
            warning = {"warning": f"Schema for index '{index_name}' not found."}

        result = self.redisSearchService.add_document(index_name, document_id, fields)
        if warning:
            result["warning"] = warning
        return result
