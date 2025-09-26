from typing import Dict, Any
from pydantic_settings import BaseSettings



class OnlineConfig(BaseSettings):
    """本地开发环境配置"""
    
    # 应用设置
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    # 数据库设置 - 本地开发环境
    DATABASE_URLS: Dict[str, str] = {
        "default": "mysql+aiomysql://root:123456@localhost:3306/vegas",  # 默认数据库
        "ro": "mysql+aiomysql://root:123456@localhost:3306/vegas",      # 只读数据库
        "rw": "mysql+aiomysql://root:123456@localhost:3306/vegas",      # 读写数据库
    }
    
    # Redis设置 - 本地开发环境
    REDIS_CONF: Dict[str, Dict[str, Any]] = {
        "vegas": {
            "host": "localhost",
            "port": 6379,
            "db_id": 0
        },
        "vegas_fb": {
            "host": "localhost", 
            "port": 6379,
            "db_id": 1
        }
    }
    
    # JWT设置 - 本地环境（较短的过期时间用于测试）
    #python -c "import secrets; print(secrets.token_urlsafe(32))"
    JWT_SECRET_KEY: str = "5TUbuxOwBtKS5ukoKxJ2OBUAqReGuaoMl2OTqElVFn0"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 3
    
    # CORS设置 - 本地环境允许所有来源
    ALLOW_ORIGINS: list = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list = ["*"]
    ALLOW_HEADERS: list = ["*"]
    
    
    # 本地环境特有配置
    ENABLE_DOCS: bool = True  # 启用API文档
    ENABLE_TEST_ROUTES: bool = True  # 启用测试路由


        # API设置
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Payment API"
    PROJECT_VERSION: str = "2.0.0"


settings = OnlineConfig()