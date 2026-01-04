from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pgvector.sqlalchemy import Vector
from models.knowledge import Knowledge
from services.gemini_service import gemini_service
from typing import List

class VectorService:
    async def add_knowledge(self, db: AsyncSession, content: str, source: str = None):
        vector = await gemini_service.get_embedding(content)
        knowledge = Knowledge(content=content, vector=vector, source=source)
        db.add(knowledge)
        await db.commit()
        await db.refresh(knowledge)
        return knowledge

    async def search_similar(self, db: AsyncSession, query_text: str, limit: int = 3) -> List[Knowledge]:
        query_vector = await gemini_service.get_embedding(query_text)
        # Using cosine distance for similarity search
        stmt = select(Knowledge).order_by(Knowledge.vector.cosine_distance(query_vector)).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

vector_service = VectorService()
