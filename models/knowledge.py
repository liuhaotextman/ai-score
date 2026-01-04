from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer
from pgvector.sqlalchemy import Vector
from core.database import Base

class Knowledge(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    vector: Mapped[list] = mapped_column(Vector(768)) # Gemini text-embedding-004 is usually 768 dims
    source: Mapped[str] = mapped_column(Text, nullable=True)
