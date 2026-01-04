from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# Construct async connection string for psycopg3
# postgresql+psycopg://user:pass@host:port/dbname
DATABASE_URL = f"postgresql+psycopg://{settings.PgSQL.User}:{settings.PgSQL.Pass}@{settings.PgSQL.Host}:{settings.PgSQL.Port}/{settings.PgSQL.DB}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
