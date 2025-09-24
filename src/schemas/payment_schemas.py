
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


# ===== 基础模型 =====
class UserBase(SQLModel):
    """用户基础模型"""
    uid: Optional[str] = Field(default=None, description="用户ID")
    user_name: Optional[str] = Field(default=None, description="用户名")
    level: Optional[int] = Field(default=None, description="用户等级")
    coins: Optional[str] = Field(default=None, description="金币数")
    cash: Optional[str] = Field(default=None, description="第三货币数")
    avatar_url: Optional[str] = Field(default=None, description="头像URL")
    show: Optional[int] = Field(default=None, description="是否展示商店")


class OrderBase(SQLModel):
    """订单基础模型"""
    order_id: str = Field(..., description="订单ID")
    uid: str = Field(..., description="用户ID")
    item_id: int = Field(..., description="商品ID")
    price: float = Field(..., description="价格")
    currency: str = Field(..., description="币种")


class PaymentBase(SQLModel):
    """支付基础模型"""
    payment_channel: str = Field(..., description="支付渠道")
    payment_method: str = Field(..., description="支付方式: card|paypal|apple pay")
    ip: str = Field(..., description="IP地址")
    country: str = Field(..., description="国家")


class ResponseBase(SQLModel):
    """响应基础模型"""
    return_code: Optional[int] = Field(default=None, description="返回码: 1=成功, 0=失败")
    status_code: Optional[int] = Field(default=None, description="状态码: 1=成功, 0=失败")
    err_code: Optional[int] = Field(default=None, description="错误码")
    msg: Optional[str] = Field(default=None, description="消息")


# ===== 登录相关 =====
class LoginRequest(SQLModel):
    login_type: int = Field(..., description="登录类型: 1=facebook, 2=google, 3=usertoken, 4=email, 5=sms, 6=apple")
    login_id: str = Field(..., description="登录ID")
    login_code: Optional[str] = Field(None, description="验证码(邮箱/SMS登录时需要)")
    share_id: Optional[str] = Field(None, description="邀请者ID(可选)")


class LoginResponse(ResponseBase, UserBase):
    daily_gift: Optional[int] = Field(default=None, description="每日礼物状态: 0=不可领取, 1=可领取")


# ===== 每日礼物相关 =====
class DailyGiftRequest(SQLModel):
    uid: str = Field(..., description="用户ID")


class DailyGiftResponse(ResponseBase):
    pass


# ===== 商城相关 =====
class ActItem(SQLModel):
    """附加商品/礼包"""
    id: int = Field(..., description="商品ID")
    name: str = Field(..., description="商品名称")
    num: int = Field(..., description="数量")


class StoreItem(SQLModel):
    """商城商品"""
    id: int = Field(..., description="商品ID")
    default_price: float = Field(..., description="默认价格(美元)")
    tokens: int = Field(..., description="发放奖品数")
    tokens_base: int = Field(..., description="活动前数量")
    bonus: float = Field(..., description="活动百分比")
    act_items: List[ActItem] = Field(default_factory=list, description="附加商品列表")


class StoreItemsRequest(SQLModel):
    uid: str = Field(..., description="用户ID")


class StoreItemsResponse(ResponseBase):
    is_first_pay: Optional[int] = Field(default=None, description="是否首次充值: 0=否, 1=是")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="商品列表")


# ===== 支付成功相关 =====
class PaymentSuccessRequest(OrderBase, PaymentBase):
    custom_param: Optional[str] = Field(None, description="自定义参数")
    email: str = Field(..., description="邮箱")


class PaymentSuccessResponse(ResponseBase):
    pass


# ===== 支付失败相关 =====
class PaymentFailureRequest(OrderBase, PaymentBase):
    web_lang: Optional[str] = Field(None, description="网页语言")
    browser_lang: Optional[str] = Field(None, description="浏览器语言")
    web_pay_error_code: str = Field(..., description="报错原因")


class PaymentFailureResponse(ResponseBase):
    pass


# ===== 订单历史相关 =====
class OrderHistoryRequest(SQLModel):
    uid: str = Field(..., description="用户ID")


class OrderDetail(SQLModel):
    """订单详情"""
    order_id: str = Field(..., description="订单ID")
    item_name: str = Field(..., description="商品名称")
    order_time: str = Field(..., description="订单时间")
    order_status: str = Field(..., description="订单状态")
    price: Optional[float] = Field(None, description="价格")
    currency: Optional[str] = Field(None, description="币种")


class OrderHistoryResponse(ResponseBase):
    data: List[Dict[str, Any]] = Field(default_factory=list, description="订单数据列表")


# ===== Token相关 =====
class TokenRequest(SQLModel):
    """Token获取请求"""
    appId: Optional[str] = Field(default=None, description="应用ID")
    # 可以根据需要添加其他自定义参数


class TokenResponse(ResponseBase):
    """Token获取响应"""
    token: Optional[str] = Field(default=None, description="访问令牌，有效期3小时")


# ===== 刷新用户信息相关 =====
class RefreshUserInfoRequest(SQLModel):
    """刷新用户信息请求"""
    uid: str = Field(..., description="用户ID")


class RefreshUserInfoResponse(ResponseBase, UserBase):
    daily_gift: Optional[int] = Field(default=None, description="每日礼物状态: 0=不可领取, 1=可领取")
