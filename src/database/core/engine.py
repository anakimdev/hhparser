from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database.configs import settings

async_engine = create_async_engine(
    url = settings.database_url_asyncpg,
    echo = True
)

async_session = async_sessionmaker(bind=async_engine)