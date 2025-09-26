from typing import Dict, Any
from pydantic_settings import BaseSettings


class OnlineConfig(BaseSettings):
    """生产环境配置"""
    
    # 应用设置
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    
    # 数据库设置 - 生产环境（读写分离）
    DATABASE_URLS: Dict[str, str] = {
        "default": "mysql+aiomysql://payment_user:prod_password@prod-db-master:3306/vegas_production",
        "ro": "mysql+aiomysql://payment_user:prod_password@prod-db-slave:3306/vegas_production",   # 只读从库
        "rw": "mysql+aiomysql://payment_user:prod_password@prod-db-master:3306/vegas_production",  # 读写主库
    }
    
    # Redis设置 - 生产环境（集群配置）
    REDIS_CONF: Dict[str, Dict[str, Any]] = {
        "vegas": {
            "host": "redis-cluster-vegas.prod.internal",
            "port": 6379,
            "db_id": 0,
        },
        "vegas_fb": {
            "host": "redis-cluster-vegas.prod.internal", 
            "port": 6379,
            "db_id": 1,
        }
    }
    
    # JWT设置
    #python -c "import secrets; print(secrets.token_urlsafe(32))"
    JWT_SECRET_KEY: str = "5TUbuxOwBtKS5ukoKxJ2OBUAqReGuaoMl2OTqElVFn0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 3
    
    # CORS设置 - 生产环境限制域名
    ALLOW_ORIGINS: list = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list = ["GET", "POST", "PUT", "DELETE"]
    ALLOW_HEADERS: list = ["Content-Type", "Authorization"]
    
    # 生产环境特有配置
    ENABLE_DOCS: bool = False  # 生产环境禁用API文档
    ENABLE_TEST_ROUTES: bool = False  # 生产环境禁用测试路由


    # API设置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Payment API"
    PROJECT_VERSION: str = "2.0.0"

settings = OnlineConfig()

