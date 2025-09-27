from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas.document import IndexDocumentRequest
from app.services.document_service import DocumentService
from app.schemas.response import create_success_response, create_error_response
from app.configs.settings import settings

import time
import json

router = APIRouter()

document_service = DocumentService()

@router.post("/")
def index_document(req: IndexDocumentRequest):
    index_name = document_service.index_document(
        index_name=f"idx:{req.schema_name.lower()}",
        document_id=req.document_id,
        fields=req.fields
    )

    return create_success_response(
        data={
            "index_name": index_name
        },
        message="Document indexed successfully"
    )

@router.get("/search/")
def search_documents(
    schema_name: str,
    term: str,
    background_tasks: BackgroundTasks,
    limit: int = 10,
    offset: int = 0,
):
    start_time = time.perf_counter()

    result = document_service.search_documents(
        index_name=f"idx:{schema_name.lower()}",
        term=term,
        limit=limit,
        offset=offset
    )

    end_time = time.perf_counter()
    duration_ms = (end_time - start_time) * 1000

    background_tasks.add_task(
        document_service.log_search,
        redis_index_name=f"idx:{schema_name.lower()}",
        parameters=json.dumps({"term": term, "limit": limit, "offset": offset}),
        duration_ms=duration_ms
    )

    return create_success_response(
        data=result,
        message="Search completed successfully"
    )