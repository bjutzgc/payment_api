"""
支付处理服务模块
处理支付成功和失败的业务逻辑
完全基于新的 WebchargePaymentLog 模型，不再依赖旧版 WebStore
"""
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from datetime import datetime
import logging
import json

from ..models import User, WebchargePaymentLog
from .db_service import get_session
from .redis_service import get_redis_db_user
from ..item_configs import get_item_tokens, is_high_level_user
from .game_service import send_reward_to_inbox

logger = logging.getLogger("payment_api")


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
                return {"success": False, "error": "订单已处理"}
            
            # 2. 获取或创建用户信息
            user = self._get_user(uid)
            if not user:
                user = self._create_test_user(uid)
                logger.info(f"Created test user - UID: {uid}")
            
            # 3. 检查用户是否为首充用户（购买次数为0）
            is_first_charge = user.purchase_count == 0
            
            # 4. 根据用户状态计算实际获得的第三货币数量
            tokens = get_item_tokens(
                item_id=item_id,
                user_coins=user.coins,
                user_level=float(user.level),
                is_first_charge=is_first_charge
            )
            
            # 5. 检查用户是否有权限购买该商品（7-8号商品需要高级用户）
            if item_id > 6 and not is_high_level_user(user.coins, float(user.level)):
                logger.warning(f"User {uid} cannot access high-level item {item_id}")
                return {"success": False, "error": "该商品仅对高级用户开放"}
            
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
            user.coins += tokens
            user.purchase_count += 1
            
            # 8. 提交数据库事务
            self.session.add(payment_log)
            self.session.add(user)
            self.session.commit()
            
            # 9. 发送奖励到收件箱
            reward_reason = f"购买{item_id}号商品奖励"
            if is_first_charge:
                reward_reason += "（首充奖励）"
            
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
            return {"success": False, "error": f"处理失败: {str(e)}"}
    
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
            return {"success": False, "error": f"处理失败: {str(e)}"}
    
    def _get_payment_log(self, order_id: str) -> Optional[WebchargePaymentLog]:
        """获取支付日志信息"""
        statement = select(WebchargePaymentLog).where(WebchargePaymentLog.order_id == order_id)
        return self.session.exec(statement).first()
    
    def _get_user(self, user_id: int) -> Optional[User]:
        """获取用户信息"""
        statement = select(User).where(User.id == user_id)
        return self.session.exec(statement).first()
    
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
    with get_session(pkg) as session:
        processor = PaymentProcessor(session)
        return processor.process_payment_success(payment_data)


def process_payment_failure(payment_data: Dict[str, Any], pkg: str = 'default') -> Dict[str, Any]:
    """处理支付失败的便捷函数"""
    with get_session(pkg) as session:
        processor = PaymentProcessor(session)
        return processor.process_payment_failure(payment_data)


def get_payment_history(user_id: int, limit: int = 50, pkg: str = 'default') -> list:
    """获取用户支付历史"""
    try:
        with get_session(pkg) as session:
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
        