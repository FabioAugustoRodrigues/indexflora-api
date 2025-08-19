from pydantic import BaseModel
from typing import Dict, Any

class IndexDocumentRequest(BaseModel):
    schema_name: str
    document_id: str
    fields: Dict[str, Any]
