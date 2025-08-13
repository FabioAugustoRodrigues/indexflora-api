from pydantic import BaseModel
from typing import List

class FieldDefinition(BaseModel):
    name: str
    type: str
    sortable: bool = False
    weight: float = 1.0

class CreateSchemaRequest(BaseModel):
    name: str
    fields: List[FieldDefinition]
