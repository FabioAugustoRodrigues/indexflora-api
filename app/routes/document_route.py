from fastapi import APIRouter, HTTPException

from app.schemas.document import IndexDocumentRequest
from app.services.redis_search_service import RedisSearchService

router = APIRouter()
redisSearchService = RedisSearchService(host="redis", port=6379)

@router.post("/")
def index_document(req: IndexDocumentRequest):
    try:
        redis_result = redisSearchService.add_document(
            index_name=f"idx:{req.schema_name.lower()}",
            document_id=req.document_id,
            fields=req.fields
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was an error indexing: {e}")

    return {
        "message": "Document indexed successfully",
        "redisearch": redis_result
    }
