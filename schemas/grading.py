from pydantic import BaseModel

class GradeRequest(BaseModel):
    question: str
    answer: str

class GradeResponse(BaseModel):
    score: int
    reason: str
    context_used: str
