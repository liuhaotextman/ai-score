from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.vector_service import vector_service
from schemas.knowledge import KnowledgeCreate, KnowledgeResponse
from typing import List

router = APIRouter()

@router.post("/knowledge", response_model=KnowledgeResponse)
async def add_knowledge(item: KnowledgeCreate, db: AsyncSession = Depends(get_db)):
    return await vector_service.add_knowledge(db, item.content, item.source)

@router.post("/knowledge/upload")
async def upload_knowledge_file(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db)
):
    # Only support text files for now
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Only .txt or .md files are supported")
    
    try:
        content = await file.read()
        text = content.decode("utf-8")
        
        # Split by double newline or a reasonable length to avoid too huge chunks
        # This is a simple strategy, can be improved later
        chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 10]
        
        results = []
        for chunk in chunks:
            kb_item = await vector_service.add_knowledge(db, chunk, file.filename)
            results.append(kb_item.id)
            
        return {"filename": file.filename, "chunks_processed": len(results), "ids": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

@router.get("/knowledge/search", response_model=List[KnowledgeResponse])
async def search_knowledge(query: str, limit: int = 3, db: AsyncSession = Depends(get_db)):
    return await vector_service.search_similar(db, query, limit)
