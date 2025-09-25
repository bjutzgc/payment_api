"""
登录服务模块
处理不同类型的用户登录逻辑
"""
from typing import Optional
from sqlmodel import Session, select
import logging

from ..models import User, AccountInfo
from ..constants import (
    ACCOUNT_TYPE_FACEBOOK, ACCOUNT_TYPE_GOOGLE, ACCOUNT_TYPE_APPLE
)
from .db_service import get_session

logger = logging.getLogger("payment_api")

from datetime import datetime, timezone
from authlib.jose import jwt, JoseError
import time


USER_TOKEN_SECRET_KEY = "oye9cVw6rJPb3AR512HjP_cEbuFKsC7_fHFdrimylnE"  # 生产环境使用强密码
USER_TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60  # token有效期60分钟


def verify_user_token(token: str):
    """
    验证JWT token（时间戳版本）
    """
    try:
        claims = jwt.decode(token, USER_TOKEN_SECRET_KEY)
        current_ts = int(time.time())
        
        # 手动验证过期时间
        if 'exp' in claims and claims['exp'] < current_ts:
            return {
                'success': False,
                'error': 'Token expired',
                'expired_at': datetime.fromtimestamp(claims['exp'], timezone.utc)
            }
        
        return {
            'success': True,
            'user_id': claims['user_id'],
            'issued_at': datetime.fromtimestamp(claims['iat'], timezone.utc),
            'expires_at': datetime.fromtimestamp(claims['exp'], timezone.utc),
            'remaining_time': claims['exp'] - current_ts  # 剩余秒数
        }
        
    except JoseError as e:
        return {
            'success': False,
            'error': f'Token verification failed: {str(e)}'
        }


def get_user_id_from_token(token: str):
    """
    从JWT token中获取用户ID
    """
    payload = verify_user_token(token)
    if payload and 'success' in payload and payload['success']:
        return payload['user_id']
    return None

class LoginType:
    """登录类型常量"""
    FACEBOOK = 1
    GOOGLE = 2
    USER_TOKEN = 3
    EMAIL = 4
    SMS = 5
    APPLE = 6


def find_user_by_login(login_type: int, login_id: str, pkg: str = 'default') -> Optional[User]:
    """
    根据登录类型和登录ID查找用户
    
    Args:
        login_type: 登录类型 (1=Facebook, 2=Google, 3=UserToken, 4=Email, 5=SMS, 6=Apple)
        login_id: 登录ID
        pkg: 数据库包名/类型 (向后兼容)
    
    Returns:
        User: 找到的用户对象，如果没找到返回None
    """
    try:
        with get_session(pkg) as session:
            if login_type == LoginType.FACEBOOK:
                # Facebook登录：从User表中查找facebook_id
                return _find_user_by_facebook_id(session, login_id)
            
            elif login_type == LoginType.GOOGLE:
                # Google登录：从AccountInfo表中查找account_type=GOOGLE的记录
                return _find_user_by_account_info(session, ACCOUNT_TYPE_GOOGLE, login_id)
            
            elif login_type == LoginType.APPLE:
                # Apple登录：从AccountInfo表中查找account_type=APPLE的记录
                return _find_user_by_account_info(session, ACCOUNT_TYPE_APPLE, login_id)
            
            elif login_type == LoginType.USER_TOKEN:
                return _find_user_by_token(session, user_token=login_id)
            
            elif login_type == LoginType.EMAIL:
                # Email登录：暂未实现
                logger.warning(f"Email login not implemented: {login_id}")
                return None
            
            elif login_type == LoginType.SMS:
                # SMS登录：暂未实现
                logger.warning(f"SMS login not implemented: {login_id}")
                return None
            
            else:
                logger.error(f"Unsupported login type: {login_type}")
                return None
                
    except Exception as e:
        logger.error(f"Error finding user - LoginType: {login_type}, LoginId: {login_id}, Error: {str(e)}")
        return None


def find_user_by_uid(uid: str, pkg: str = 'default') -> Optional[User]:
    """
    根据用户ID查找用户
    
    Args:
        uid: 用户ID
        pkg: 数据库包名/类型 (向后兼容)
    
    Returns:
        User: 找到的用户对象，如果没找到返回None
    """
    try:
        with get_session(pkg) as session:
            statement = select(User).where(User.id == int(uid))
            user = session.exec(statement).first()
            
            if user:
                logger.info(f"User found by UID: User ID: {user.id}")
            else:
                logger.warning(f"User not found: UID={uid}")
            
            return user
    except Exception as e:
        logger.error(f"Error finding user by UID: UID={uid}, Error: {str(e)}")
        return None


def _find_user_by_facebook_id(session: Session, facebook_id: str) -> Optional[User]:
    """
    通过Facebook ID查找用户
    
    Args:
        session: 数据库会话
        facebook_id: Facebook ID
    
    Returns:
        User: 找到的用户对象，如果没找到返回None
    """
    try:
        statement = select(User).where(User.facebook_id == facebook_id)
        users = session.exec(statement).all()
        
        if not users:
            logger.info(f"Facebook user not found: {facebook_id}")
            return None
        elif len(users) == 1:
            logger.info(f"Facebook user found: {facebook_id}")
            return users[0]
        else:
            # 多个设备用户，获取最后登录的
            logger.warning(f"Multiple Facebook user records found, selecting the last logged in user: {facebook_id}")
            latest_user = None
            for user in users:
                if latest_user is None or user.last_login > latest_user.last_login:
                    latest_user = user
            return latest_user
            
    except Exception as e:
        logger.error(f"Error finding Facebook user: {facebook_id}, Error: {str(e)}")
        return None


def _find_user_by_account_info(session: Session, account_type: int, account_id: str) -> Optional[User]:
    """
    通过AccountInfo表查找用户
    
    Args:
        session: 数据库会话
        account_type: 账户类型 (2=Facebook, 3=Apple, 5=Google)
        account_id: 第三方账户ID
    
    Returns:
        User: 找到的用户对象，如果没找到返回None
    """
    try:
        # 先从AccountInfo表中查找账户信息
        account_statement = select(AccountInfo).where(
            AccountInfo.account_type == account_type,
            AccountInfo.account_id == account_id
        )
        account_info = session.exec(account_statement).first()
        
        if not account_info:
            account_type_name = {
                ACCOUNT_TYPE_GOOGLE: "Google",
                ACCOUNT_TYPE_APPLE: "Apple"
            }.get(account_type, f"Unknown({account_type})")
            logger.info(f"{account_type_name} account info not found: {account_id}")
            return None
        
        # 根据primary_user_id查找用户
        user_statement = select(User).where(User.id == account_info.primary_user_id)
        user = session.exec(user_statement).first()
        
        if user:
            account_type_name = {
                ACCOUNT_TYPE_GOOGLE: "Google",
                ACCOUNT_TYPE_APPLE: "Apple"
            }.get(account_type, f"Unknown({account_type})")
            logger.info(f"{account_type_name} user found: {account_id} -> User ID: {user.id}")
        else:
            logger.warning(f"AccountInfo exists but User not found: AccountType={account_type}, AccountId={account_id}, UserId={account_info.primary_user_id}")
        
        return user
        
    except Exception as e:
        logger.error(f"Error finding user through AccountInfo: AccountType={account_type}, AccountId={account_id}, Error: {str(e)}")
        return None


def _find_user_by_token(session: Session, user_token: str) -> Optional[User]:
    """
    通过UserToken查找用户
    
    Args:
        session: 数据库会话
        user_token: 用户Token
    
    Returns:
        User: 找到的用户对象，如果没找到返回None
    """
    try:
        # 从 token 中解析用户ID
        user_id = get_user_id_from_token(user_token)
        if not user_id:
            logger.warning(f"Token parsing failed or invalid: {user_token[:20]}...")
            return None
        
        # 从User表中查找用户
        statement = select(User).where(User.id == int(user_id))
        user = session.exec(statement).first()
        
        if user:
            logger.info(f"User found through token: User ID: {user.id}")
        else:
            logger.warning(f"User ID from token does not exist: {user_id}")
        
        return user
        
    except Exception as e:
        logger.error(f"Error finding user through token: {str(e)}")
        return None


def validate_login_params(login_type: int, login_id: str, login_code: Optional[str] = None) -> bool:
    """
    验证登录参数
    
    Args:
        login_type: 登录类型
        login_id: 登录ID
        login_code: 验证码 (邮箱/SMS登录时需要)
        user_token: 用户Token (UserToken登录时需要)
    
    Returns:
        bool: 参数是否有效
    """
    # 验证登录类型是否有效
    valid_login_types = [
        LoginType.FACEBOOK, LoginType.GOOGLE, LoginType.USER_TOKEN,
        LoginType.EMAIL, LoginType.SMS, LoginType.APPLE
    ]
    
    if login_type not in valid_login_types:
        logger.error(f"Invalid login type: {login_type}")
        return False
    
    # 验证登录ID是否为空
    if not login_id or login_id.strip() == "":
        logger.error(f"Login ID cannot be empty")
        return False
    
    # 验证码登录需要验证码
    if login_type in [LoginType.EMAIL, LoginType.SMS] and not login_code:
        logger.error(f"Email and SMS login require verification code")
        return False
    
    return True