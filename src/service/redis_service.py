import redis
from typing import Dict, Optional
from ..web_config import settings
import logging

logger = logging.getLogger("payment_api")

# Redis连接池字典
REDIS: Dict[str, redis.Redis] = {}


def create_redis_pool():
    """创建Redis连接池"""
    if not settings.REDIS_CONF:
        logger.warning("No Redis configuration found")
        return
        
    for pkg_info, info in settings.REDIS_CONF.items():
        try:
            redis_host = info['host']
            redis_port = info['port'] 
            redis_db = info['db_id']
            redis_pool = redis.ConnectionPool(
                host=redis_host, 
                port=redis_port, 
                db=redis_db, 
                max_connections=500
            )
            REDIS[pkg_info] = redis.Redis(connection_pool=redis_pool)
            logger.info(f"Redis pool created for {pkg_info}")
        except Exception as e:
            logger.error(f"Failed to create Redis pool for {pkg_info}: {e}")


def get_redis_db_user(pkg: str = 'vegas') -> Optional[redis.Redis]:
    """获取用户相关的Redis连接"""
    return REDIS.get(f'{pkg}_user')


def get_redis_db_fb(pkg: str = 'vegas_fb') -> Optional[redis.Redis]:
    """获取Facebook相关的Redis连接"""
    return REDIS.get(f'{pkg}_fb')


# 初始化Redis连接池
create_redis_pool()