from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


# ===== 基础模型 =====
class UserBase(SQLModel):
    """用户基础模型"""
    uid: Optional[str] = Field(default=None, description="User ID")
    user_name: Optional[str] = Field(default=None, description="Username")
    level: Optional[int] = Field(default=None, description="User level")
    coins: Optional[str] = Field(default=None, description="Coin count")
    cash: Optional[str] = Field(default=None, description="Token count")
    avatar_url: Optional[str] = Field(default=None, description="Avatar URL")
    show: Optional[int] = Field(default=None, description="Whether to show store")


class OrderBase(SQLModel):
    """订单基础模型"""
    order_id: str = Field(..., description="Order ID")
    uid: str = Field(..., description="User ID")
    item_id: int = Field(..., description="Item ID")
    price: float = Field(..., description="Price")
    currency: str = Field(..., description="Currency")


class PaymentBase(SQLModel):
    """支付基础模型"""
    payment_channel: str = Field(..., description="Payment channel")
    payment_method: str = Field(..., description="Payment method: card|paypal|apple pay")
    ip: str = Field(..., description="IP address")
    country: str = Field(..., description="Country")


class ResponseBase(SQLModel):
    """响应基础模型"""
    return_code: Optional[int] = Field(default=None, description="Return code: 1=success, 0=failure")
    status_code: Optional[int] = Field(default=None, description="Status code: 1=success, 0=failure")
    err_code: Optional[int] = Field(default=None, description="Error code")
    msg: Optional[str] = Field(default=None, description="Message")


# ===== 登录相关 =====
class LoginRequest(SQLModel):
    login_type: int = Field(..., description="Login type: 1=facebook, 2=google, 3=usertoken, 4=email, 5=sms, 6=apple")
    login_id: str = Field(..., description="Login ID")
    login_code: Optional[str] = Field(None, description="Verification code (required for email/SMS login)")
    share_id: Optional[str] = Field(None, description="Inviter ID (optional)")


class LoginResponse(ResponseBase, UserBase):
    daily_gift: Optional[int] = Field(default=None, description="Daily gift status: 0=not claimable, 1=claimable")


# ===== 每日礼物相关 =====
class DailyGiftRequest(SQLModel):
    uid: str = Field(..., description="User ID")


class DailyGiftResponse(ResponseBase):
    pass


# ===== 商城相关 =====
class ActItem(SQLModel):
    """附加商品/礼包"""
    id: int = Field(..., description="Item ID")
    name: str = Field(..., description="Item name")
    num: int = Field(..., description="Quantity")


class StoreItemsRequest(SQLModel):
    uid: str = Field(..., description="User ID")


class StoreItemsResponse(ResponseBase):
    is_first_pay: Optional[int] = Field(default=None, description="First payment: 0=no, 1=yes")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="Item list")


# ===== 支付成功相关 =====
class PaymentSuccessRequest(OrderBase, PaymentBase):
    custom_param: Optional[str] = Field(None, description="Custom parameter")
    email: str = Field(..., description="Email")


class PaymentSuccessResponse(ResponseBase):
    pass


# ===== 支付失败相关 =====
class PaymentFailureRequest(OrderBase, PaymentBase):
    web_lang: Optional[str] = Field(None, description="Web language")
    browser_lang: Optional[str] = Field(None, description="Browser language")
    web_pay_error_code: str = Field(..., description="Error reason")


class PaymentFailureResponse(ResponseBase):
    pass


# ===== 订单历史相关 =====
class OrderHistoryRequest(SQLModel):
    uid: str = Field(..., description="User ID")


class OrderDetail(SQLModel):
    """订单详情"""
    order_id: str = Field(..., description="Order ID")
    item_name: str = Field(..., description="Item name")
    order_time: str = Field(..., description="Order time")
    order_status: str = Field(..., description="Order status")
    price: Optional[float] = Field(None, description="Price")
    currency: Optional[str] = Field(None, description="Currency")


class OrderHistoryResponse(ResponseBase):
    data: List[Dict[str, Any]] = Field(default_factory=list, description="Order data list")


# ===== Token相关 =====
class TokenRequest(SQLModel):
    """Token获取请求"""
    appId: Optional[str] = Field(default=None, description="App ID")
    # 可以根据需要添加其他自定义参数


class TokenResponse(ResponseBase):
    """Token获取响应"""
    token: Optional[str] = Field(default=None, description="Access token, valid for 3 hours")


# ===== 刷新用户信息相关 =====
class RefreshUserInfoRequest(SQLModel):
    """刷新用户信息请求"""
    uid: str = Field(..., description="User ID")


class RefreshUserInfoResponse(ResponseBase, UserBase):
    daily_gift: Optional[int] = Field(default=None, description="Daily gift status: 0=not claimable, 1=claimable")