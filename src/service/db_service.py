from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from typing import Dict, Any, AsyncGenerator, Optional
from ..web_config import settings

engines: Dict[str, Any] = {}
async_engines: Dict[str, AsyncEngine] = {}
default_engine = None
default_async_engine = None


def create_engine_for_url(database_url: str, echo: bool = False):
    if 'mysql+aiomysql' in database_url or 'postgresql+asyncpg' in database_url:
        async_engine = create_async_engine(
            database_url, 
            echo=echo,
            pool_recycle=3600,
            pool_pre_ping=True
        )

        if 'mysql+aiomysql' in database_url:
            sync_url = database_url.replace('mysql+aiomysql', 'mysql+pymysql')
        elif 'postgresql+asyncpg' in database_url:
            sync_url = database_url.replace('postgresql+asyncpg', 'postgresql+psycopg2')
        else:
            sync_url = database_url
        
        sync_engine = create_engine(
            sync_url, 
            echo=echo,
            pool_recycle=3600,
            pool_pre_ping=True
        )
        return sync_engine, async_engine
    else:
        sync_engine = create_engine(
            database_url, 
            echo=echo,
            pool_recycle=3600,
            pool_pre_ping=True
        )
        return sync_engine, None


def init_database_engines():
    global default_engine, default_async_engine
    for db_type, database_url in settings.DATABASE_URLS.items():
        sync_engine, async_engine = create_engine_for_url(database_url, echo=settings.DEBUG)
        
        engines[db_type] = sync_engine
        if async_engine:
            async_engines[db_type] = async_engine
        
        if db_type == 'default' or (default_engine is None):
            default_engine = sync_engine
            default_async_engine = async_engine


init_database_engines()


def get_session(db_type: str = 'default') -> Session:
    if db_type not in engines and db_type not in ['default', 'ro', 'rw', 'analytics']:
        db_type = 'default'
    
    engine = engines.get(db_type, default_engine)
    if engine is None:
        raise ValueError(f"No engine found for database type '{db_type}'")
    return Session(engine)


async def get_async_session(db_type: str = 'default') -> AsyncGenerator[AsyncSession, None]:
    engine = async_engines.get(db_type, default_async_engine)
    if engine is None:
        raise ValueError(f"No async engine found for database type '{db_type}'")
    
    async with AsyncSession(engine) as session:
        yield session


def get_engine(db_type: str = 'default'):
    return engines.get(db_type, default_engine)


def get_async_engine(db_type: str = 'default') -> Optional[AsyncEngine]:
    return async_engines.get(db_type, default_async_engine)


def get_available_databases() -> Dict[str, str]:
    return settings.DATABASE_URLS.copy()


def get_readonly_session() -> Session:
    return get_session('ro')


async def get_readonly_async_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_async_session('ro'):
        yield session


def get_readwrite_session() -> Session:
    return get_session('rw')


async def get_readwrite_async_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_async_session('rw'):
        yield session