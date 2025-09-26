from fastapi import APIRouter, HTTPException

from app.schemas.document import IndexDocumentRequest
from app.services.document_service import DocumentService
from app.schemas.response import create_success_response, create_error_response
from app.configs.settings import settings

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
    limit: int = 10,
    offset: int = 0
):
    return create_success_response(
        data=document_service.search_documents(
            index_name=f"idx:{schema_name.lower()}",
            term=term,
            limit=limit,
            offset=offset
        ),
        message="Search completed successfully"
    )