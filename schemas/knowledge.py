from pydantic import BaseModel
from typing import Optional

class KnowledgeCreate(BaseModel):
    content: str
    source: Optional[str] = None

class KnowledgeResponse(BaseModel):
    id: int
    content: str
    source: Optional[str] = None
    embedding_model: str

    class Config:
        from_attributes = True
