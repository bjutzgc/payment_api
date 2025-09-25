from fastapi import APIRouter, HTTPException, Query, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
import logging
from datetime import datetime, timedelta
from authlib.jose import jwt
from authlib.jose.errors import InvalidTokenError
import secrets

from ..schemas.payment_schemas import (
    LoginRequest, LoginResponse, 
    DailyGiftRequest, DailyGiftResponse,
    StoreItemsRequest, StoreItemsResponse,
    PaymentSuccessRequest, PaymentSuccessResponse,
    PaymentFailureRequest, PaymentFailureResponse,
    OrderHistoryRequest, OrderHistoryResponse,
    TokenRequest, TokenResponse,
    RefreshUserInfoRequest, RefreshUserInfoResponse
)
from ..web_config import settings
from ..constants import *
from ..service.login_service import find_user_by_login, validate_login_params, find_user_by_uid
from ..service.payment_service import process_payment_success, process_payment_failure, get_payment_history, get_item_name, get_available_store_items
from ..service.game_service import get_user_ext

logger = logging.getLogger("payment_api")

router = APIRouter(prefix="/api/v1")

# Token相关配置
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
TOKEN_EXPIRY_HOURS = settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS

# HTTP Bearer验证器
security = HTTPBearer()

DEBUG_SHOW = 0

def create_access_token(data: dict) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    to_encode.update({"exp": expire})
    header = {'alg': ALGORITHM}
    encoded_jwt = jwt.encode(header, to_encode, SECRET_KEY)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """验证令牌"""
    try:
        claims = jwt.decode(credentials.credentials, SECRET_KEY)
        return dict(claims)
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_client_info(request: Request) -> Dict[str, str]:
    """获取客户端信息"""
    # 获取真实 IP地址（考虑代理和负载均衡）
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.headers.get("X-Real-IP", request.client.host if request.client else "unknown")
    
    # 获取国家信息（可以通过IP地址库查询，这里简化处理）
    country = request.headers.get("CF-IPCountry", "US")  # Cloudflare提供的国家信息
    
    # 获取用户代理信息
    user_agent = request.headers.get("User-Agent", "")
    
    # 获取语言信息
    accept_language = request.headers.get("Accept-Language", "")
    
    return {
        "ip": client_ip,
        "country": country,
        "user_agent": user_agent,
        "accept_language": accept_language
    }


@router.post("/token", response_model=TokenResponse)
async def get_token(request: TokenRequest):
    """
    获取访问令牌接口（有效期3小时）
    
    自定义参数示例：
    - appId: 应用ID
    - 可根据需要添加其他参数
    """
    try:
        logger.info(f"Token request - AppId: {request.appId}")
        if request.appId != APP_ID:
            return TokenResponse(
                return_code=0,
                msg="Invalid AppId"
            )
        
        # 生成令牌载荷
        token_data = {
            "appId": request.appId,
            "issued_at": datetime.utcnow().isoformat(),
            "token_id": secrets.token_hex(16)  # 唯一标识
        }
        
        # 创建令牌
        access_token = create_access_token(token_data)
        
        response = TokenResponse(
            return_code=1,
            token=access_token,
            msg="Token generation successful"
        )
        
        logger.info(f"Token generated successfully - AppId: {request.appId}")
        return response
        
    except Exception as e:
        logger.error(f"Token generation error: {str(e)}")
        return TokenResponse(
            return_code=0,
            msg=f"Token generation failed: {str(e)}"
        )


@router.get("/login", response_model=LoginResponse)
async def login(
    login_type: int = Query(..., description="登录类型: 1=facebook, 2=google, 3=usertoken, 4=email, 5=sms, 6=apple"),
    login_id: str = Query(..., description="登录ID"),
    login_code: Optional[str] = Query(None, description="验证码(邮箱/SMS登录时需要)"),
    share_id: Optional[str] = Query(None, description="邀请者ID(可选)")
):
    """
    用户登录接口 (GET 方法)
    
    支持多种登录方式：
    1. Facebook登录 (login_type=1, login_id=facebook_id)
    2. Google登录 (login_type=2, login_id=google_id) 
    3. UserToken登录 (login_type=3, login_id=usertoken)
    4. 邮箱登录 (login_type=4, login_id=email, 需要 login_code)
    5. SMS登录 (login_type=5, login_id=phone, 需要 login_code)
    6. Apple ID登录 (login_type=6, login_id=apple_id)
    
    URL 参数：
    - login_type: 登录类型 (1-6)
    - login_id: 登录ID
    - login_code: 验证码(邮箱/SMS登录时需要)
    - share_id: 邀请者ID(可选)
    """
    try:
        logger.info(f"Login attempt - Type: {login_type}, ID: {login_id}, ShareId: {share_id}")
        
        # 验证登录参数
        if not validate_login_params(login_type, login_id, login_code=login_code):
            return LoginResponse(
                status_code=0,
                msg="Invalid login parameters"
            )
        
        # 根据登录类型查找用户
        user = find_user_by_login(login_type, login_id)
        
        if not user:
            # 用户不存在，返回登录失败
            logger.warning(f"User not found - Type: {login_type}, ID: {login_id}")
            return LoginResponse(
                status_code=0,
                msg="User not found"
            )
        user_ext = get_user_ext(user.id)
        show = DEBUG_SHOW
        user_total_purchase = 0.0
        cash = 0.0
        if user_ext:
            user_total_purchase = user_ext.get(K_USER_TOTAL_PURCHASE, 0.0)
            if 300 < user_total_purchase < 2000:
                if (user.id // 10000) % 10 == 0:
                    show = 1
            cash = user_ext.get(K_USER_CASH, 0.0) + user_ext.get(K_USER_CASH_FREE, 0.0)
                
        coins = (-user.coins * 1000000000) if user.coins < 0 else user.coins
        # 用户存在，生成成功登录响应
        response = LoginResponse(
            status_code=1,
            uid=str(user.id),
            user_name=user.facebook_name or f"User_{user.id}",
            level=user.level,
            coins= str(coins),
            cash=str(cash / 100),
            daily_gift=1,  # 1表示可以领取每日礼物（需要根据实际逻辑判断）
            avatar_url="https://example.com/avatar.jpg",  # 可以根据用户信息设置
            msg="Login successful",
            show=show,
        )
        
        logger.info(f"Login successful - UserID: {user.id}, LoginType: {login_type}")
        return response
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return LoginResponse(
            status_code=0,
            msg=f"Login failed: {str(e)}"
        )


@router.post("/daily_gift", response_model=DailyGiftResponse)
async def claim_daily_gift(request: DailyGiftRequest):
    """
    领取每日奖励接口
    """
    try:
        logger.info(f"Daily gift claim request - UID: {request.uid}")
        
        # TODO: 实现每日礼物领取逻辑
        # 检查用户是否存在
        # 检查是否已经领取
        # 检查是否符合领取条件
        
        # 模拟成功响应
        response = DailyGiftResponse(
            return_code=1
        )
        
        logger.info(f"Daily gift claimed successfully - UID: {request.uid}")
        return response
        
    except Exception as e:
        logger.error(f"Daily gift claim error: {str(e)}")
        return DailyGiftResponse(
            return_code=0,
            err_code=999  # 系统错误
        )


@router.post("/store/items", response_model=StoreItemsResponse)
async def get_store_items(request: StoreItemsRequest):
    """
    获取商城商品列表接口（支持动态商品配置）
    根据用户等级和金币数量决定商品数量
    """
    try:
        logger.info(f"Store items request - UID: {request.uid}")
        
        user = find_user_by_uid(request.uid)
        # 默认值（如果用户不存在或者访问失败）
        user_coins = 0
        user_level = 1.0
        
        if user:
            user_coins = user.coins
            user_level = float(user.level)
            is_first_charge_user = user.purchase_count == 0
            logger.info(f"User found - UID: {user.id}, Coins: {user_coins}, Level: {user_level}, FirstCharge: {is_first_charge_user}")
        else:
            logger.info(f"User not found - UID: {request.uid}, using default values")
        
        # 获取用户可用的商品列表
        items = get_available_store_items(user)
        
        response = StoreItemsResponse(
            return_code=1,
            is_first_pay=0,
            items=items
        )
        
        logger.info(f"Store items returned - UID: {request.uid}, Items count: {len(items)}, FirstCharge: {is_first_charge_user}")
        return response
        
    except Exception as e:
        logger.error(f"Store items error: {str(e)}")
        return StoreItemsResponse(
            return_code=0,
            is_first_pay=0,
            items=[]
        )


@router.post("/payment/success", response_model=PaymentSuccessResponse)
async def payment_success(request: PaymentSuccessRequest, fastapi_request: Request, token_data: dict = Depends(verify_token)):
    """
    支付成功回调接口（支持动态奖励计算）
    
    需要在Headers中添加:
    Authorization: Bearer {token}
    """
    try:
        logger.info(f"Payment success - OrderID: {request.order_id}, UID: {request.uid}, ItemID: {request.item_id}, TokenData: {token_data.get('appId')}")
        
        # 获取客户端信息
        client_info = get_client_info(fastapi_request)
        
        # 准备支付数据（不再预先计算tokens，由payment_service动态计算）
        payment_data = {
            "order_id": request.order_id,
            "uid": request.uid,
            "item_id": request.item_id,
            "price": request.price,
            "currency": request.currency,
            "ip": client_info["ip"],
            "country": client_info["country"],
            "payment_method": request.payment_method,
            "email": request.email
        }
        
        # 处理支付成功（内部会根据用户状态动态计算奖励）
        result = process_payment_success(payment_data)
        
        if result["success"]:
            tokens_granted = result.get('tokens_granted', 0)
            is_first_charge = result.get('is_first_charge', False)
            purchase_count = result.get('purchase_count', 0)
            
            msg = f"Payment successful, rewards distributed! Received {tokens_granted} tokens"
            if is_first_charge:
                msg += " (First charge bonus)"
            
            response = PaymentSuccessResponse(
                return_code=1,
                msg=msg
            )
            logger.info(f"Payment processed successfully - OrderID: {request.order_id}, Tokens: {tokens_granted}, FirstCharge: {is_first_charge}, PurchaseCount: {purchase_count}")
        else:
            response = PaymentSuccessResponse(
                return_code=0,
                err_code=500,
                msg=result.get("error", "Processing failed")
            )
            logger.error(f"Payment processing failed - OrderID: {request.order_id}, Error: {result.get('error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Payment success processing error: {str(e)}")
        return PaymentSuccessResponse(
            return_code=0,
            err_code=500,
            msg=f"Processing failed: {str(e)}"
        )


@router.post("/payment/failure", response_model=PaymentFailureResponse)
async def payment_failure(request: PaymentFailureRequest, fastapi_request: Request, token_data: dict = Depends(verify_token)):
    """
    支付失败记录接口
    
    需要在Headers中添加:
    Authorization: Bearer {token}
    """
    try:
        logger.info(f"Payment failure - OrderID: {request.order_id}, UID: {request.uid}, Error: {request.web_pay_error_code}, TokenData: {token_data.get('appId')}")
        
        # 获取客户端信息
        client_info = get_client_info(fastapi_request)
        
        # 准备支付数据
        payment_data = {
            "order_id": request.order_id,
            "uid": request.uid,
            "item_id": request.item_id,
            "web_pay_error_code": request.web_pay_error_code,
            "web_lang": request.web_lang,
            "browser_lang": request.browser_lang,
            "ip": client_info["ip"],
            "country": client_info["country"],
            "payment_method": request.payment_method
        }
        
        # 处理支付失败
        result = process_payment_failure(payment_data)
        
        if result["success"]:
            response = PaymentFailureResponse(
                return_code=1,
                msg="Payment failure recorded"
            )
            logger.info(f"Payment failure recorded - OrderID: {request.order_id}, Error: {request.web_pay_error_code}")
        else:
            response = PaymentFailureResponse(
                return_code=0,
                err_code=500,
                msg=result.get("error", "Recording failed")
            )
            logger.error(f"Payment failure recording failed - OrderID: {request.order_id}, Error: {result.get('error')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Payment failure processing error: {str(e)}")
        return PaymentFailureResponse(
            return_code=0,
            err_code=500,
            msg=f"Recording failed: {str(e)}"
        )


@router.post("/orders/history", response_model=OrderHistoryResponse)
async def get_order_history(request: OrderHistoryRequest):
    """
    获取订单历史记录接口
    """
    try:
        logger.info(f"Order history request - UID: {request.uid}")
        
        # 获取用户的支付历史
        payment_history = get_payment_history(int(request.uid), limit=50)
        
        # 转换为订单历史格式
        orders = []
        for payment in payment_history:
            order_status = "completed" if payment["status"] == 1 else "failed"
            
            # 使用商品配置获取商品名称
            try:
                item_id = int(payment['item_id'])
                item_name = get_item_name(item_id)
            except (ValueError, TypeError):
                item_name = f"Unknown item {payment['item_id']}"
            
            orders.append({
                "order_id": payment["order_id"],
                "item_name": item_name,
                "order_time": payment["created_at"],
                "order_status": order_status,
                "price": payment["price"],
                "currency": payment["currency"]
            })
        
        response = OrderHistoryResponse(
            status_code=1,
            data=orders
        )
        
        logger.info(f"Order history returned - UID: {request.uid}, Orders count: {len(orders)}")
        return response
        
    except Exception as e:
        logger.error(f"Order history error: {str(e)}")
        return OrderHistoryResponse(
            status_code=0,
            data=[],
            msg=f"Failed to retrieve: {str(e)}"
        )


@router.post("/refresh", response_model=RefreshUserInfoResponse)
async def refresh_user_info(
    request: RefreshUserInfoRequest,
    token_data: dict = Depends(verify_token)
):
    """
    刷新用户信息接口 (POST 方法)
    
    只需要提供用户ID和认证Token
    
    Headers:
    - Authorization: Bearer {token}
    
    Request Body:
    {
        "uid": "user_id"     # 用户ID
    }
    
    响应格式与登录接口相同
    """
    try:
        logger.info(f"Refresh user info attempt - UID: {request.uid}")
        
        # 根据用户ID查找用户
        user = find_user_by_uid(request.uid)
        
        if not user:
            # 用户不存在，返回失败
            logger.warning(f"User not found for refresh - UID: {request.uid}")
            return RefreshUserInfoResponse(
                status_code=0,
                msg="User not found"
            )
        
        # 生成并返回登录响应
        response = _generate_refresh_response(user)
        logger.info(f"User info refreshed successfully - UserID: {user.id}")
        return response
        
    except Exception as e:
        logger.error(f"Refresh user info error: {str(e)}")
        return RefreshUserInfoResponse(
            status_code=0,
            msg=f"Refresh failed: {str(e)}"
        )

def _generate_refresh_response(user):
    """生成刷新用户信息响应的通用函数"""
    try:
        user_ext = get_user_ext(user.id)
        show = DEBUG_SHOW
        user_total_purchase = 0.0
        cash = 0.0
        if user_ext:
            user_total_purchase = user_ext.get(K_USER_TOTAL_PURCHASE, 0.0)
            if 300 < user_total_purchase < 2000:
                if (user.id // 10000) % 10 == 0:
                    show = 1
            cash = user_ext.get(K_USER_CASH, 0.0) + user_ext.get(K_USER_CASH_FREE, 0.0)
                
        coins = (-user.coins * 1000000000) if user.coins < 0 else user.coins
        
        # 用户存在，生成成功响应
        response = RefreshUserInfoResponse(
            status_code=1,
            uid=str(user.id),
            user_name=user.facebook_name or f"User_{user.id}",
            level=user.level,
            coins=str(coins),
            cash=str(cash / 100),
            daily_gift=1,  # 1表示可以领取每日礼物（需要根据实际逻辑判断）
            avatar_url="https://example.com/avatar.jpg",  # 可以根据用户信息设置
            msg="Refresh successful",
            show=show,
        )
        
        return response
    except Exception as e:
        logger.error(f"Generate refresh response error: {str(e)}")
        return RefreshUserInfoResponse(
            status_code=0,
            msg=f"Failed to generate response: {str(e)}"
        )
