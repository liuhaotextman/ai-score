from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from core.database import Base

class GradingResult(Base):
    __tablename__ = "grading_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    context_used: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
