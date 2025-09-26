"""
支付处理服务模块
处理支付成功和失败的业务逻辑
完全基于新的 WebchargePaymentLog 模型，不再依赖旧版 WebStore
"""
from typing import Optional, Dict, Any
from sqlalchemy import Select, func
from sqlmodel import Session, select
from datetime import datetime
import logging
import json

from ..constants import *
from ..models import User, WebchargePaymentLog, UserExt
from .db_service import get_readonly_session, get_readwrite_session
from .redis_service import get_redis_db_user
from .game_service import send_reward_to_inbox

logger = logging.getLogger("payment_api")


STORE_ITEMS_CONFIG = [
    {
        "id": 8,
        "price": 999.99,
        "name": "Mythic Pack",
        "normal_bonus": 0.06,
        "base_tokens": 1000,
        "first_bonus": 0.25
    },
    {
        "id": 7,
        "price": 599.99,
        "name": "Legend Pack",
        "normal_bonus": 0.05,
        "base_tokens": 600,
        "first_bonus": 0.25
    },
    {
        "id": 6,
        "price": 399.99,
        "name": "Deluxe Pack",
        "normal_bonus": 0.04,
        "base_tokens": 400,
        "first_bonus": 0.25
    },
    {
        "id": 5,
        "price": 199.99,
        "name": "Premium Pack",
        "normal_bonus": 0.02,
        "base_tokens": 200,
        "first_bonus": 0.15
    },
    {
        "id": 4,
        "price": 99.99,
        "name": "Elite Pack",
        "normal_bonus": 0.01,
        "base_tokens": 100,
        "first_bonus": 0.15
    },
    {
        "id": 3,
        "price": 49.99,
        "name": "Advanced Pack",
        "normal_bonus": 0,
        "base_tokens": 50,
        "first_bonus": 0.1
    },
    {
        "id": 2,
        "price": 29.99,
        "name": "Growth Pack",
        "normal_bonus": 0,
        "base_tokens": 30,
        "first_bonus": 0.1
    },
    {
        "id": 1,
        "price": 19.99,
        "name": "Starter Pack",
        "normal_bonus": 0,
        "base_tokens": 20,
        "first_bonus": 0.1
    }
]

def calculate_tokens(base_tokens: int, bonus_rate: float) -> int:
    bonus_tokens = int(base_tokens * bonus_rate)
    return base_tokens + bonus_tokens


def is_high_level_user(user) -> bool:
    return False
#   return user_coins >= 10000 and user_level >= 99.99


def get_available_store_items(user) -> list:
    # Determine the number of items based on user level
    if is_high_level_user(user):
        # High-level user: 8 items
        available_items = STORE_ITEMS_CONFIG[2:]
    else:
        # Regular user: first 6 items
        available_items = STORE_ITEMS_CONFIG[2:]
    
    # Build the response data
    items = []
    with get_readonly_session() as session:
        for item in available_items:
            count = session.scalar(
                select(func.coalesce(func.count(WebchargePaymentLog.id), 0))
                .where(
                    WebchargePaymentLog.uid == user.id,
                    WebchargePaymentLog.item_id == item["id"]
                )
            ) or 0
            actual_tokens = calculate_tokens(item["base_tokens"], item["normal_bonus"] if count else item["first_bonus"])
            
            items.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "tokens": actual_tokens,
                "base_tokens": item["base_tokens"],
                "bonus_rate": item["normal_bonus"] ,
                "first_rate": item["first_bonus"] if not count else 0.0,
                "act_items": []  # Additional items, can be configured as needed
            })
    
    return items


def get_item_config(item_id, user, is_first_charge):
    for item in STORE_ITEMS_CONFIG:
        if item["id"] == item_id:
            # Check if the user can access this item
            if item_id > 6 and not is_high_level_user(user):
                # Regular users cannot access items 7-8
                return {
                    "name": f"Unavailable Item {item_id}",
                    "tokens": 0,
                    "base_tokens": 0,
                    "bonus_percent": 0
                }
            
            # Use normal_bonus
            bonus_rate = item["normal_bonus"] if not is_first_charge else item["first_bonus"]
            actual_tokens = calculate_tokens(item["base_tokens"], bonus_rate)
            
            return {
                "name": item["name"],
                "tokens": actual_tokens,
                "base_tokens": item["base_tokens"],
                "bonus_percent": int(bonus_rate * 100)
            }

    # Default configuration
    return {
        "name": f"Unknown Item {item_id}",
        "tokens": 100,  # Default 100 tokens
        "base_tokens": 100,
        "bonus_percent": 0
    }


def get_item_tokens(item_id, user, is_first_charge):
    config = get_item_config(item_id, user, is_first_charge)
    return config["tokens"]


def get_item_name(item_id: int) -> str:
    # First check the new configuration
    for item in STORE_ITEMS_CONFIG:
        if item["id"] == item_id:
            return item["name"]
    
    return f"unknown item {item_id}"


class PaymentStatus:
    """支付状态常量"""
    SUCCESS = 1
    FAILED = 0
    PENDING = 2
    CANCELLED = 3
    REFUNDED = 4


class PaymentProcessor:
    """支付处理器 - 完全基于 WebchargePaymentLog"""
    
    def __init__(self, session: Session):
        self.session = session
        self.redis_client = get_redis_db_user()
    
    def process_payment_success(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付成功逻辑"""
        order_id = None
        try:
            order_id = payment_data.get('order_id', '')
            uid = int(payment_data.get('uid', 0))
            item_id = payment_data.get('item_id', 0)
            price = float(payment_data.get('price', 0.0))
            currency = payment_data.get('currency', 'USD')
            ip = payment_data.get('ip', '')
            country = payment_data.get('country', '')
            payment_method = payment_data.get('payment_method', 'unknown')
            email = payment_data.get('email')
            
            logger.info(f"Processing payment success - OrderID: {order_id}, UID: {uid}, ItemID: {item_id}")
            
            # 1. 检查订单是否已经处理过
            existing_log = self._get_payment_log(order_id)
            if existing_log and existing_log.status == PaymentStatus.SUCCESS:
                logger.warning(f"Order already processed - OrderID: {order_id}")
                return {"success": False, "error": "Order already processed"}
            
            # 2. 获取或创建用户信息
            user = self._get_user(uid)
            if not user:
                user = self._create_test_user(uid)
                logger.info(f"Created test user - UID: {uid}")

            # 3. 检查用户是否为首充用户（购买次数为0）
            is_first_charge = self._get_first_charge(user.id, item_id=item_id)
            
            # 4. 根据用户状态计算实际获得的第三货币数量
            tokens = get_item_tokens(item_id, user, is_first_charge)
            
            # 5. 检查用户是否有权限购买该商品（7-8号商品需要高级用户）
            if item_id > 6 and not is_high_level_user(user):
                logger.warning(f"User {uid} cannot access high-level item {item_id}")
                return {"success": False, "error": "This item is only available to premium users"}
            
            logger.info(f"Calculated tokens - ItemID: {item_id}, Tokens: {tokens}, IsFirstCharge: {is_first_charge}")
            
            # 6. 记录支付成功日志
            payment_log = self._create_payment_log(
                order_id=order_id,
                uid=str(uid),
                item_id=str(item_id),
                price=price,
                currency=currency,
                ip=ip,
                country=country,
                payment_method=payment_method,
                email=email,
                status=PaymentStatus.SUCCESS
            )
            
            # 7. 更新用户金币和购买次数
            old_coins = user.coins
            
            # 8. 提交数据库事务
            self.session.add(payment_log)
            self.session.commit()
            
            self._set_user_cash(uid, tokens)
            # 9. 发送奖励到收件箱
            reward_reason = f"Reward for purchasing item {item_id}"
            if is_first_charge:
                reward_reason += " (First charge bonus)"

            
            inbox_success = send_reward_to_inbox('default', uid, tokens, reward_reason)
            if not inbox_success:
                logger.warning(f"Failed to send reward to inbox - OrderID: {order_id}, UID: {uid}")
            
            logger.info(f"Payment success processed - OrderID: {order_id}, Tokens: {tokens}, FirstCharge: {is_first_charge}, InboxSent: {inbox_success}")
            
            return {
                "success": True,
                "user_id": uid,
                "order_id": order_id,
                "item_id": item_id,
                "tokens_granted": tokens,
                "old_coins": old_coins,
                "new_coins": user.coins,
                "is_first_charge": is_first_charge,
                "purchase_count": user.purchase_count
            }
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Payment success processing error - OrderID: {order_id}, Error: {str(e)}")
            return {"success": False, "error": f"Processing failed: {str(e)}"}
    
    def process_payment_failure(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付失败逻辑"""
        order_id = None
        try:
            order_id = payment_data.get('order_id', '')
            uid = int(payment_data.get('uid', 0))
            item_id = payment_data.get('item_id', 0)
            error_code = payment_data.get('web_pay_error_code', 'UNKNOWN_ERROR')
            web_lang = payment_data.get('web_lang')
            browser_lang = payment_data.get('browser_lang')
            ip = payment_data.get('ip', '')
            country = payment_data.get('country', '')
            payment_method = payment_data.get('payment_method', 'unknown')
            
            logger.info(f"Processing payment failure - OrderID: {order_id}, UID: {uid}, Error: {error_code}")
            
            # 记录支付失败日志
            payment_log = self._create_payment_log(
                order_id=order_id,
                uid=str(uid),
                item_id=str(item_id),
                price=0.0,
                currency='USD',
                ip=ip,
                country=country,
                payment_method=payment_method,
                status=PaymentStatus.FAILED,
                web_lang=web_lang,
                browser_lang=browser_lang,
                web_pay_error_code=error_code
            )
            
            self.session.add(payment_log)
            self.session.commit()
            
            logger.info(f"Payment failure processed - OrderID: {order_id}, Error: {error_code}")
            
            return {
                "success": True,
                "user_id": uid,
                "order_id": order_id,
                "error_code": error_code,
                "failure_recorded": True
            }
            
        except Exception as e:
            self.session.rollback()
            logger.error(f"Payment failure processing error - OrderID: {order_id}, Error: {str(e)}")
            return {"success": False, "error": f"Processing failed: {str(e)}"}
    
    def _get_payment_log(self, order_id: str) -> Optional[WebchargePaymentLog]:
        """获取支付日志信息"""
        statement = select(WebchargePaymentLog).where(WebchargePaymentLog.order_id == order_id)
        return self.session.exec(statement).first()
    
    def _get_user(self, user_id: int) -> Optional[User]:
        """获取用户信息"""
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()

    def _set_user_cash(self, user_id, tokens):
        cash=self.redis_client.get("jwins_cash_" + str(user_id))
        if cash:
            self.redis_client.set("jwins_cash_" + str(user_id), int(cash) + tokens)
        else:
            self.redis_client.set("jwins_cash_" + str(user_id), tokens)

    def _get_first_charge(self, user_id: int, item_id) -> int:
        """获取用户第一次充值的额外奖励"""
        count = self.session.scalar(
                select(func.coalesce(func.count(WebchargePaymentLog.id), 0))
                .where(
                    WebchargePaymentLog.uid == user_id,
                    WebchargePaymentLog.item_id == item_id
                )
            ) or 0
        return count <= 0
    
    def _create_test_user(self, user_id: int) -> User:
        """创建测试用户"""
        user = User(
            id=user_id,
            facebook_id=f"test_user_{user_id}",
            package="com.funtriolimited.slots.casino.free",
            facebook_name=f"Test User {user_id}",
            coins=0,
            level=1,
            vip_level=1,
            first_login=datetime.utcnow(),
            last_login=datetime.utcnow(),
            purchase_count=0
        )
        self.session.add(user)
        return user
    
    def _create_payment_log(self, **kwargs) -> WebchargePaymentLog:
        """创建支付日志"""
        return WebchargePaymentLog(
            order_id=kwargs.get('order_id', ''),
            uid=kwargs.get('uid', ''),
            item_id=kwargs.get('item_id', ''),
            price=kwargs.get('price', 0.0),
            currency=kwargs.get('currency', 'USD'),
            ip=kwargs.get('ip', ''),
            country=kwargs.get('country', ''),
            payment_channel=kwargs.get('payment_channel', 'appcharge'),
            payment_method=kwargs.get('payment_method', 'unknown'),
            email=kwargs.get('email'),
            status=kwargs.get('status', PaymentStatus.PENDING),
            web_lang=kwargs.get('web_lang'),
            browser_lang=kwargs.get('browser_lang'),
            web_pay_error_code=kwargs.get('web_pay_error_code'),
            ext=kwargs.get('ext')
        )


def process_payment_success(payment_data: Dict[str, Any], pkg: str = 'default') -> Dict[str, Any]:
    """处理支付成功的便捷函数"""
    with get_readwrite_session() as session:
        processor = PaymentProcessor(session)
        return processor.process_payment_success(payment_data)


def process_payment_failure(payment_data: Dict[str, Any], pkg: str = 'default') -> Dict[str, Any]:
    """处理支付失败的便捷函数"""
    with get_readwrite_session() as session:
        processor = PaymentProcessor(session)
        return processor.process_payment_failure(payment_data)


def get_payment_history(user_id: int, limit: int = 50, pkg: str = 'default') -> list:
    """获取用户支付历史"""
    try:
        with get_readonly_session() as session:
            statement = select(WebchargePaymentLog).where(
                WebchargePaymentLog.uid == str(user_id)
            ).limit(limit)
            
            logs = session.exec(statement).all()
            
            # 手动按时间排序
            sorted_logs = sorted(logs, key=lambda x: x.created_at, reverse=True)
            
            return [
                {
                    "order_id": log.order_id,
                    "item_id": log.item_id,
                    "price": log.price,
                    "currency": log.currency,
                    "status": log.status,
                    "payment_method": log.payment_method,
                    "created_at": log.created_at.isoformat(),
                    "error_code": log.web_pay_error_code
                }
                for log in sorted_logs
            ]
            
    except Exception as e:
        logger.error(f"Failed to get payment history - UID: {user_id}, Error: {str(e)}")
        return []
        