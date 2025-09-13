from fastapi import APIRouter, HTTPException

from app.schemas.document import IndexDocumentRequest
from app.services.redis_search_service import RedisSearchService
from app.services.document_indexer_service import DocumentIndexerService

router = APIRouter()

redisSearchService = RedisSearchService(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
documentIndexerService = DocumentIndexerService(redisSearchService)

@router.post("/")
def index_document(req: IndexDocumentRequest):
    try:
        result = documentIndexerService.index_document(
            index_name=f"idx:{req.schema_name.lower()}",
            document_id=req.document_id,
            fields=req.fields
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was an error indexing: {e}")

    return {
        "message": "Document indexed successfully",
        "redisearch": result
    }

@router.get("/search/")
def search_documents(
    schema_name: str,
    term: str,
    limit: int = 10,
    offset: int = 0
):
    try:
        redis_result = redisSearchService.search_documents(
            index_name=f"idx:{schema_name.lower()}",
            term=term,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"There was an error searching: {e}")

    return {
        "message": "Search completed successfully",
        "redisearch": redis_result
    }