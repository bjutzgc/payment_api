from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy import Text, JSON
from typing import Optional, ClassVar
from datetime import datetime
import json


class User(SQLModel, table=True):
    __tablename__: ClassVar[str] = "user"  # type: ignore
    
    id: int = Field(primary_key=True)
    facebook_id: str = Field(default='', max_length=64)
    package: str = Field(default='', max_length=64)
    facebook_name: str = Field(default='', max_length=256)
    coins: int = Field(default=0)
    level: int = Field(default=1)
    vip_level: int = Field(default=1)
    first_login: datetime
    last_login: datetime
    purchase_count: int = Field(default=0)

class UserExt(SQLModel, table=True):
    __tablename__: ClassVar[str] = "user_ext"  # type: ignore
    id: int = Field(primary_key=True)
    user_id: int = Field(unique=True)
    data: Optional[str] = None
    last_login: datetime = Field(default_factory=datetime.utcnow)

class ActControl(SQLModel, table=True):
    __tablename__: ClassVar[str] = "act_control"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    act_type: int = Field(default=0)
    start_ts: datetime
    end_ts: datetime
    params: str = Field(default='', max_length=32)


class Inbox(SQLModel, table=True):
    __tablename__: ClassVar[str] = "inbox"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    type: int = Field(default=0)
    count: int = Field(default=0)
    ts: datetime
    valid_time_sec: int
    msg: Optional[str] = Field(default=None, max_length=512)
    resource: Optional[str] = Field(default=None, max_length=512)
    extra_data: Optional[str] = Field(default=None, sa_column=Column(Text))


class InboxLog(SQLModel, table=True):
    __tablename__: ClassVar[str] = "inbox_log"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    type: int = Field(default=0)
    count: int = Field(default=0)
    create_ts: datetime = Field(default_factory=datetime.utcnow)
    gm_name: Optional[str] = Field(default=None, max_length=64)


class FacebookEmail(SQLModel, table=True):
    __tablename__: ClassVar[str] = "facebook_email"  # type: ignore
    
    id: int = Field(primary_key=True)
    email: str = Field(default='', max_length=64)


class UserLounge(SQLModel, table=True):
    __tablename__: ClassVar[str] = "user_lounge"  # type: ignore
    
    id: int = Field(primary_key=True)
    end_ts: int = Field(default=0)


class WebStore(SQLModel, table=True):
    __tablename__: ClassVar[str] = "web_store"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str = Field(unique=True, max_length=32)
    user_id: int = Field(index=True)
    facebook_id: str = Field(default='', max_length=64)
    create_ts: int = Field(default=0)
    price: float = Field(default=0.0)
    coins: int = Field(default=0)
    coupon_id: Optional[int] = None
    state: int = Field(default=0)
    ext: Optional[str] = None


class AccountInfo(SQLModel, table=True):
    """账户信息表"""
    __tablename__: ClassVar[str] = "account_info"  # type: ignore
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: str = Field(default='', max_length=128)  # 第三方账户ID
    account_name: str = Field(default='', max_length=64)  # 账户名称
    account_type: int = Field(default=0)  # 账户类型：0=未知, 1=游客, 2=Facebook, 3=Apple, 4=华为, 5=Google
    primary_user_id: int = Field(index=True)  # 关联的用户ID
    create_ts: datetime = Field(default_factory=datetime.utcnow)  # 创建时间
    ext: Optional[str] = None  # 扩展信息




class WebchargePaymentLog(SQLModel, table=True):
    __tablename__ = "webcharge_payment_logs"  # type: ignore

    id: int = Field(default=None, primary_key=True)

    order_id: str = Field(max_length=64, nullable=False)
    uid: str = Field(max_length=64, nullable=False)
    item_id: str = Field(max_length=64, nullable=False)

    price: float = Field(nullable=False)  # 使用 float，也可改为 Decimal
    currency: str = Field(max_length=3, nullable=False)

    ip: str = Field(max_length=45, nullable=False)
    country: str = Field(max_length=2, nullable=False)

    payment_channel: str = Field(max_length=32, default="appcharge", nullable=False)
    payment_method: str = Field(max_length=32, nullable=False)

    email: Optional[str] = Field(max_length=255, default=None)

    # 支付状态: 1=success, 0=failed（或其他整数状态码）
    status: Optional[int] = Field(default=None)

    # 失败专用字段
    web_lang: Optional[str] = Field(max_length=10, default=None)
    browser_lang: Optional[str] = Field(max_length=10, default=None)
    web_pay_error_code: Optional[str] = Field(default=None, sa_column=Column(Text))

    # 可扩展字段（JSON）
    ext: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    # 时间字段
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False
    )
    