from pydantic import BaseModel, Field
from typing import List, Literal

class FieldDefinition(BaseModel):
    name: str
    type: Literal["text", "numeric", "tag"]
    sortable: bool = False
    weight: float = 1.0

class CreateSchemaRequest(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_]+$", description="Schema name must be alphanumeric/underscore")
    fields: List[FieldDefinition]
