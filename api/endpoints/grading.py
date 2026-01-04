from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.vector_service import vector_service
from services.gemini_service import gemini_service
from schemas.grading import GradeRequest, GradeResponse
from models.grading import GradingResult
import json
import re

router = APIRouter()

@router.post("/grade", response_model=GradeResponse)
async def grade_answer(request: GradeRequest, db: AsyncSession = Depends(get_db)):
    # 1. Search for relevant context
    similar_docs = await vector_service.search_similar(db, request.question, limit=3)
    context = "\n".join([doc.content for doc in similar_docs])
    
    # 2. Call Gemini to grade
    raw_result = await gemini_service.generate_score(request.question, request.answer, context)
    
    # 3. Parse result (Gemini might return markdown json blocks)
    try:
        # Extract JSON from potential markdown code block
        json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
        else:
            data = json.loads(raw_result)
        
        score = data.get("score", 0)
        reason = data.get("reason", "无法解析评语")

        # 4. Save to Database
        result_record = GradingResult(
            question=request.question,
            answer=request.answer,
            score=score,
            reason=reason,
            context_used=context
        )
        db.add(result_record)
        await db.commit()
        await db.refresh(result_record)
        
        return GradeResponse(
            score=score,
            reason=reason,
            context_used=context
        )
    except Exception as e:
        # Even in error, we might want to log it, but for now just return error response
        return GradeResponse(
            score=0,
            reason=f"解析结果失败: {str(e)}. 原始输出: {raw_result}",
            context_used=context
        )
