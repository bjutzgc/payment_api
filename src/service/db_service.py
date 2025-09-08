from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from typing import Dict, Any, AsyncGenerator, Optional
from ..web_config import settings

# 支持多数据库配置
engines: Dict[str, Any] = {}  # 同步引擎
async_engines: Dict[str, AsyncEngine] = {}  # 异步引擎
default_engine = None
default_async_engine = None


def create_engine_for_url(database_url: str, echo: bool = False):
    """为给定的URL创建数据库引擎"""
    if 'mysql+aiomysql' in database_url or 'postgresql+asyncpg' in database_url:
        # 异步引擎
        async_engine = create_async_engine(database_url, echo=echo)
        
        # 为表创建创建同步版本
        if 'mysql+aiomysql' in database_url:
            sync_url = database_url.replace('mysql+aiomysql', 'mysql+pymysql')
        elif 'postgresql+asyncpg' in database_url:
            sync_url = database_url.replace('postgresql+asyncpg', 'postgresql+psycopg2')
        else:
            sync_url = database_url
        
        sync_engine = create_engine(sync_url, echo=echo)
        return sync_engine, async_engine
    else:
        # 同步引擎（SQLite等）
        sync_engine = create_engine(database_url, echo=echo)
        return sync_engine, None


def init_database_engines():
    """初始化数据库引擎 - 支持多数据库配置"""
    global default_engine, default_async_engine
    
    # 初始化所有配置的数据库
    for db_type, database_url in settings.DATABASE_URLS.items():
        sync_engine, async_engine = create_engine_for_url(database_url, echo=settings.DEBUG)
        
        engines[db_type] = sync_engine
        if async_engine:
            async_engines[db_type] = async_engine
        
        # 设置默认引擎（优先使用'default'，其次使用第一个）
        if db_type == 'default' or (default_engine is None):
            default_engine = sync_engine
            default_async_engine = async_engine


# 初始化数据库引擎
init_database_engines()


def get_session(db_type: str = 'default') -> Session:
    """获取同步数据库会话
    
    Args:
        db_type: 数据库类型 ('default', 'ro', 'rw', 'analytics', 等)
                或者为了向后兼容，也可以是pkg参数
    """
    # 为了向后兼容，如果传入的不是标准的数据库类型，使用默认数据库
    if db_type not in engines and db_type not in ['default', 'ro', 'rw', 'analytics']:
        db_type = 'default'
    
    engine = engines.get(db_type, default_engine)
    if engine is None:
        raise ValueError(f"No engine found for database type '{db_type}'")
    return Session(engine)


async def get_async_session(db_type: str = 'default') -> AsyncGenerator[AsyncSession, None]:
    """获取异步数据库会话
    
    Args:
        db_type: 数据库类型 ('default', 'ro', 'rw', 'analytics', 等)
    """
    engine = async_engines.get(db_type, default_async_engine)
    if engine is None:
        raise ValueError(f"No async engine found for database type '{db_type}'")
    
    async with AsyncSession(engine) as session:
        yield session


def get_engine(db_type: str = 'default'):
    """获取同步数据库引擎
    
    Args:
        db_type: 数据库类型 ('default', 'ro', 'rw', 'analytics', 等)
    """
    return engines.get(db_type, default_engine)


def get_async_engine(db_type: str = 'default') -> Optional[AsyncEngine]:
    """获取异步数据库引擎
    
    Args:
        db_type: 数据库类型 ('default', 'ro', 'rw', 'analytics', 等)
    """
    return async_engines.get(db_type, default_async_engine)


def get_available_databases() -> Dict[str, str]:
    """获取所有可用的数据库配置"""
    return settings.DATABASE_URLS.copy()


def get_readonly_session() -> Session:
    """获取只读数据库会话（快捷方法）"""
    return get_session('ro')


async def get_readonly_async_session() -> AsyncGenerator[AsyncSession, None]:
    """获取只读异步数据库会话（快捷方法）"""
    async for session in get_async_session('ro'):
        yield session


def get_readwrite_session() -> Session:
    """获取读写数据库会话（快捷方法）"""
    return get_session('rw')


async def get_readwrite_async_session() -> AsyncGenerator[AsyncSession, None]:
    """获取读写异步数据库会话（快捷方法）"""
    async for session in get_async_session('rw'):
        yield session