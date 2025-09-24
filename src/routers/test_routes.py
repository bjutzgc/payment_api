from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
import logging

from ..schemas.payment_schemas import (
    LoginResponse, DailyGiftResponse, StoreItemsResponse,
    PaymentSuccessResponse, PaymentFailureResponse, OrderHistoryResponse,
    TokenResponse
)
from ..web_config import settings
from ..service.db_service import get_available_databases

logger = logging.getLogger("payment_api")

router = APIRouter()


@router.get("/simple")
async def simple_test():
    """最简单的测试接口"""
    return {
        "message": "Payment API Test Router is working", 
        "status": "ok",
        "timestamp": "2025-09-04"
    }


@router.get("/ping")
async def ping():
    """测试连通性"""
    return {"ping": "pong"}


@router.get("/login_test", response_model=LoginResponse)
async def test_login():
    """测试登录响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing login interface...")
    
    return LoginResponse(
        status_code=1,
        uid="test_user_123",
        user_name="Test User",
        level=10,
        daily_gift=1,
        avatar_url="https://example.com/avatar.jpg",
        msg="Test login successful"
    )


@router.get("/daily_gift_test", response_model=DailyGiftResponse)
async def test_daily_gift():
    """测试每日礼物响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing daily gift interface...")
    
    return DailyGiftResponse(
        return_code=1,
        msg="Test gift claim successful"
    )


@router.get("/store_items_test", response_model=StoreItemsResponse)
async def test_store_items():
    """测试商城商品列表响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing store items interface...")
    
    # 模拟商品数据
    test_items = [
        {
            "id": 1,
            "default_price": 19.99,
            "tokens": 22,
            "tokens_base": 20,
            "bonus": 10,
            "act_items": [
                {
                    "id": 100,
                    "name": "Coin Pack",
                    "num": 10
                }
            ]
        },
        {
            "id": 2,
            "default_price": 29.99,
            "tokens": 33,
            "tokens_base": 30,
            "bonus": 10,
            "act_items": []
        }
    ]
    
    return StoreItemsResponse(
        return_code=1,
        is_first_pay=1,
        items=test_items,
        msg="Test item list"
    )


@router.get("/payment_success_test", response_model=PaymentSuccessResponse)
async def test_payment_success():
    """测试支付成功响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing payment success interface...")
    
    return PaymentSuccessResponse(
        return_code=1,
        msg="Test payment successful, rewards distributed"
    )


@router.get("/payment_failure_test", response_model=PaymentFailureResponse)
async def test_payment_failure():
    """测试支付失败响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing payment failure interface...")
    
    return PaymentFailureResponse(
        return_code=1,
        err_code=500,
        msg="Test payment failure recorded"
    )


@router.get("/database_info")
async def test_database_info():
    """测试数据库配置信息"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing database configuration info...")
    
    databases = get_available_databases()
    
    return {
        "message": "Database configuration info",
        "total_databases": len(databases),
        "databases": {
            db_type: {
                "url": url,
                "type": "mysql" if "mysql" in url else "postgresql" if "postgresql" in url else "sqlite" if "sqlite" in url else "unknown",
                "async_support": "aiomysql" in url or "asyncpg" in url
            }
            for db_type, url in databases.items()
        }
    }


@router.get("/token_test", response_model=TokenResponse)
async def test_token():
    """测试Token响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing token interface...")
    
    return TokenResponse(
        return_code=1,
        token="test_token_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        msg="Test token obtained successfully"
    )


@router.get("/order_history_test", response_model=OrderHistoryResponse)
async def test_order_history():
    """测试订单历史响应数据结构"""
    if not settings.DEBUG:
        raise HTTPException(status_code=403, detail="Only available in development environment")
    
    logger.info("Testing order history interface...")
    
    # 模拟订单数据
    test_orders = [
        {
            "order_id": "test_order_001",
            "item_name": "Test Coin Pack 1000",
            "order_time": "2025-09-04 16:30:00",
            "order_status": "completed",
            "price": 19.99,
            "currency": "USD"
        },
        {
            "order_id": "test_order_002",
            "item_name": "Test Diamond Pack 500",
            "order_time": "2025-09-03 14:20:00",
            "order_status": "completed",
            "price": 29.99,
            "currency": "USD"
        }
    ]
    
    return OrderHistoryResponse(
        status_code=1,
        data=test_orders,
        msg="Test order history data"
    )