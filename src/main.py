from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .web_config import settings
from .routers.test_routes import router as test_router
from .routers.payment_routes import router as payment_router

# 配置日志
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("payment_api")


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


# 注册路由
# 测试路由只在允许的环境中注册
if getattr(settings, 'ENABLE_TEST_ROUTES', True):
    app.include_router(test_router, prefix="/test", tags=["Test"])

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