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
                # UserToken登录：暂未实现
                logger.warning(f"UserToken登录暂未实现: {login_id}")
                return None
            
            elif login_type == LoginType.EMAIL:
                # Email登录：暂未实现
                logger.warning(f"Email登录暂未实现: {login_id}")
                return None
            
            elif login_type == LoginType.SMS:
                # SMS登录：暂未实现
                logger.warning(f"SMS登录暂未实现: {login_id}")
                return None
            
            else:
                logger.error(f"不支持的登录类型: {login_type}")
                return None
                
    except Exception as e:
        logger.error(f"查找用户时发生错误 - LoginType: {login_type}, LoginId: {login_id}, Error: {str(e)}")
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
            logger.info(f"未找到Facebook用户: {facebook_id}")
            return None
        elif len(users) == 1:
            logger.info(f"找到Facebook用户: {facebook_id}")
            return users[0]
        else:
            # 多个设备用户，获取最后登录的
            logger.warning(f"发现多个Facebook用户记录，选择最后登录的用户: {facebook_id}")
            latest_user = None
            for user in users:
                if latest_user is None or user.last_login > latest_user.last_login:
                    latest_user = user
            return latest_user
            
    except Exception as e:
        logger.error(f"查找Facebook用户时发生错误: {facebook_id}, Error: {str(e)}")
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
            logger.info(f"未找到{account_type_name}账户信息: {account_id}")
            return None
        
        # 根据primary_user_id查找用户
        user_statement = select(User).where(User.id == account_info.primary_user_id)
        user = session.exec(user_statement).first()
        
        if user:
            account_type_name = {
                ACCOUNT_TYPE_GOOGLE: "Google",
                ACCOUNT_TYPE_APPLE: "Apple"
            }.get(account_type, f"Unknown({account_type})")
            logger.info(f"找到{account_type_name}用户: {account_id} -> User ID: {user.id}")
        else:
            logger.warning(f"AccountInfo存在但User不存在: AccountType={account_type}, AccountId={account_id}, UserId={account_info.primary_user_id}")
        
        return user
        
    except Exception as e:
        logger.error(f"通过AccountInfo查找用户时发生错误: AccountType={account_type}, AccountId={account_id}, Error: {str(e)}")
        return None


def validate_login_params(login_type: int, login_id: str, login_code: Optional[str] = None) -> bool:
    """
    验证登录参数
    
    Args:
        login_type: 登录类型
        login_id: 登录ID
        login_code: 验证码 (邮箱/SMS登录时需要)
    
    Returns:
        bool: 参数是否有效
    """
    # 验证登录类型是否有效
    valid_login_types = [
        LoginType.FACEBOOK, LoginType.GOOGLE, LoginType.USER_TOKEN,
        LoginType.EMAIL, LoginType.SMS, LoginType.APPLE
    ]
    
    if login_type not in valid_login_types:
        logger.error(f"无效的登录类型: {login_type}")
        return False
    
    # 验证登录ID是否为空
    if not login_id or login_id.strip() == "":
        logger.error(f"登录ID不能为空")
        return False
    
    # 验证码登录需要验证码
    if login_type in [LoginType.EMAIL, LoginType.SMS] and not login_code:
        logger.error(f"邮箱和SMS登录需要验证码")
        return False
    
    return True