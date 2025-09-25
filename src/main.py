import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .web_config import settings
from .routers.test_routes import router as test_router
from .routers.payment_routes import router as payment_router

# 配置日志
def setup_logging():
    """设置日志配置"""
    # 创建logger
    logger = logging.getLogger("payment_api")
    logger.setLevel(logging.INFO if settings.DEBUG else logging.WARNING)
    
    # 清除现有的处理器以避免重复
    logger.handlers.clear()
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO if settings.DEBUG else logging.WARNING)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # 添加控制台处理器到logger
    logger.addHandler(console_handler)
    
    # 尝试创建并添加文件处理器
    log_dir = "/var/log/slots_forever"
    try:
        # 检查目录是否存在，如果不存在则尝试创建
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, mode=0o755, exist_ok=True)
            logger.info(f"已创建日志目录: {log_dir}")
        
        # 检查是否有写入权限
        test_file = os.path.join(log_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        
        # 创建文件处理器（使用轮转日志）
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_dir, "payment_api.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO if settings.DEBUG else logging.WARNING)
        file_handler.setFormatter(formatter)
        
        # 添加文件处理器到logger
        logger.addHandler(file_handler)
        
        logger.info(f"文件日志已启用，日志文件位于: {os.path.join(log_dir, 'payment_api.log')}")
    except PermissionError:
        # 如果没有权限写入 /var/log，尝试使用用户主目录
        home_log_dir = os.path.join(os.path.expanduser("~"), "logs", "slots_forever")
        try:
            os.makedirs(home_log_dir, mode=0o755, exist_ok=True)
            file_handler = RotatingFileHandler(
                filename=os.path.join(home_log_dir, "payment_api.log"),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.INFO if settings.DEBUG else logging.WARNING)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.warning(f"无法写入 /var/log/slots_forever，日志将写入: {home_log_dir}")
        except Exception as e:
            logger.warning(f"无法设置文件日志记录: {e}")
            logger.warning("将继续使用控制台日志记录")
    except Exception as e:
        logger.warning(f"无法设置文件日志记录: {e}")
        logger.warning("将继续使用控制台日志记录")
    
    return logger

# 初始化日志
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动事件
    logger.info("Starting Payment API...")
    logger.info("Payment API started successfully")
    
    yield  # 应用运行期间
    
    # 关闭事件
    logger.info("Shutting down Payment API...")

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI version of the payment system",
    version=settings.PROJECT_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs" if getattr(settings, 'ENABLE_DOCS', True) else None,
    redoc_url="/redoc" if getattr(settings, 'ENABLE_DOCS', True) else None,
    lifespan=lifespan  # 使用新的lifespan事件处理器
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)


app.include_router(payment_router, tags=["Payment"])


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "Payment API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )