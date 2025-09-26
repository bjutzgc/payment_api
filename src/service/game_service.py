import json
import datetime
import time
from typing import Optional, List, Dict, Any
from sqlalchemy.sql.functions import user
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from ..models import User, ActControl, Inbox, FacebookEmail, UserExt, UserLounge, WebStore, InboxLog
from .db_service import get_session, get_readonly_session
from .redis_service import get_redis_db_user, get_redis_db_fb
from ..constants import *
import logging

logger = logging.getLogger("payment_api")

# 全局活动数据 (模拟thread_channel.G_ACTIVITY_DATA)
G_ACTIVITY_DATA: Dict[str, tuple] = {
    "test_activity": (
        datetime.datetime.now() - datetime.timedelta(days=1),
        datetime.datetime.now() + datetime.timedelta(days=30)
    )
}


def get_user_object(pkg: str, fb_id: str) -> Optional[User]:
    """根据Facebook ID获取用户对象"""
    if not fb_id:
        return None
    
    with get_readonly_session() as session:
        statement = (
            select(User)
            .where(User.facebook_id == fb_id)
        )
        users = session.exec(statement).all()
        
        if not users:
            return None
        elif len(users) == 1:
            return users[0]
        else:
            # 多个设备用户，获取最后登录的
            logger.warning('user_msg...multiple device users get last login.')
            fb_user = None
            for user in users:
                if fb_user is None:
                    fb_user = user
                elif user.last_login > fb_user.last_login:
                    fb_user = user
            return fb_user



def get_ext_from_db(pkg: str, user_id: str) -> Optional[UserExt]:
    """根据Facebook ID获取用户对象"""
    if not user_id:
        return None
    
    with get_readonly_session() as session:
        statement = (
            select(UserExt)
            .where(UserExt.user_id == int(user_id))
        )
        users = session.exec(statement).all()
        
        if not users:
            return None
        elif len(users) == 1:
            return users[0]
        else:
            # 多个设备用户，获取最后登录的
            logger.warning('user_msg...multiple device users ext get last login.')
            fb_user = None
            for user in users:
                if fb_user is None:
                    fb_user = user
                elif user.last_login > fb_user.last_login:
                    fb_user = user
            return fb_user


def generate_user_info(pkg: str, data: Dict[str, Any], fb_user: User):
    """生成用户信息"""
    user_id = fb_user.id
    data['user_id'] = user_id
    data['fb_name'] = fb_user.facebook_name
    data['level'] = fb_user.level
    data['vip_level'] = fb_user.vip_level
    data['max_purchase'] = fb_user.purchase_count
    data['balance'] = fb_user.coins
    data['package'] = fb_user.package
    data['login_ts'] = get_utc_ts_str(fb_user.first_login)
    data['total_purchase'] = get_total_purchase(user_id)
    data['is_online'] = get_online_status(user_id)
    data['fb_email'] = get_fb_email(pkg, user_id)
    data['is_hrc'] = get_hrc_state(pkg, user_id)
    generate_coupon_info(pkg, data, user_id)


def get_user_ext(user_id: int):
    """获取用户总购买金额"""
    redis_client = get_redis_db_user()
    user_ext = {}
    if redis_client:
        try:
            ue = redis_client.get(USER_EXT_KEY % user_id)
            if ue:
                user_ext = json.loads(ue)
        except Exception as e:
            logger.error(f"Error getting use ext: {e}")
    else:
        logger.error("Cannot get redis client for user data.")
    return user_ext


def get_total_purchase(user_id: int) -> float:
    """获取用户总购买金额"""
    user_ext = get_user_ext(user_id)
    return user_ext.get(K_USER_TOTAL_PURCHASE, 0.0)


def get_online_status(user_id: int) -> bool:
    """获取用户在线状态"""
    is_online = False
    redis_client = get_redis_db_fb()
    if redis_client:
        try:
            value = redis_client.get(USER_ONLINE_KEY % user_id)
            if value:
                is_online = True
        except Exception as e:
            logger.error(f"Error getting online status: {e}")
    else:
        logger.error("Cannot get redis client for fb data.")
    return is_online


def get_fb_email(pkg: str, user_id: int) -> Optional[str]:
    """获取Facebook邮箱"""
    with get_session(pkg) as session:
        statement = select(FacebookEmail).where(FacebookEmail.id == user_id)
        fb_email = session.exec(statement).first()
        return fb_email.email if fb_email else None


def generate_activity_info(data: Dict[str, Any]):
    """生成活动信息"""
    cur_ts = datetime.datetime.now()
    for act_name, (start_ts, end_ts) in G_ACTIVITY_DATA.items():
        if start_ts <= cur_ts < end_ts:
            data[act_name] = get_utc_ts_str(end_ts)


def generate_coupon_info(pkg: str, data: Dict[str, Any], user_id: int):
    """生成优惠券信息"""
    coupon_list = []
    cur_ts = datetime.datetime.now()
    
    with get_session(pkg) as session:
        statement = (
            select(Inbox)
            .where(Inbox.user_id == user_id)
            .where(Inbox.type.in_([9, 201, 203, 204, 205, 207]))
        )
        coupons = session.exec(statement).all()
        
        for item in coupons:
            end_ts = item.ts + datetime.timedelta(seconds=item.valid_time_sec)
            if end_ts > cur_ts:
                coupon_list.append({
                    'id': item.id, 
                    'value': item.count, 
                    'expire': get_utc_ts_str(end_ts)
                })
    
    data['coupons'] = coupon_list


def get_hrc_state(pkg: str, user_id: int) -> bool:
    """获取HRC状态"""
    is_activate = False
    with get_session(pkg) as session:
        statement = select(UserLounge).where(UserLounge.id == user_id)
        user_lounge = session.exec(statement).first()
        
        if user_lounge and user_lounge.end_ts:
            if time.time() < user_lounge.end_ts:
                is_activate = True
    
    return is_activate


def create_web_order(pkg: str, req_data: Dict[str, Any]) -> Dict[str, Any]:
    """创建Web订单"""
    fb_id: Any | None = req_data.get('fb_id')
    user_id: Any | None = req_data.get('user_id')
    order_id: Any | None = req_data.get('order_id')
    coins: Any | None = req_data.get('coins')
    price: Any | None = req_data.get('price')
    coupon_id: Any | None = req_data.get('coupon_id')
    coupon_value: Any | None = req_data.get('coupon_value')
    
    data: dict[str, Any] = {'fb_id': fb_id, 'user_id': user_id, 'status': 0}
    
    if user_id and fb_id and coins:
        try:
            coupon_id = int(coupon_id) if coupon_id else None
            coupon_value = int(coupon_value) if coupon_value else None
        except (ValueError, TypeError):
            coupon_id = None
            coupon_value = None
        
        order_status = save_order_item(
            pkg, order_id, user_id, fb_id, price, coins, coupon_id, coupon_value
        )
        
        if coupon_id:
            remove_inbox_coupon(pkg, user_id, coupon_id)
        
        if order_status == 1:
            send_online_user(user_id, order_id)
        
        data['status'] = order_status
    
    return data


def send_online_user(user_id: int, order_id: str):
    """向在线用户发送消息"""
    redis_client = get_redis_db_fb()
    if redis_client:
        try:
            value = redis_client.get(USER_ONLINE_KEY % user_id)
            if value:
                data = {'uid': user_id, 'order_id': order_id}
                logger.info(f"send_online_user ... {data}")
                # 这里原来是ZMQ发送，可以替换为其他消息队列
                # zmq_channel.socket_send(value, data)
        except Exception as e:
            logger.error(f"Error sending to online user: {e}")
    else:
        logger.error("Cannot get redis client for sending message.")


def save_order_item(
    pkg: str, 
    order_id: str, 
    user_id: int, 
    fb_id: str, 
    price: float, 
    coins: int, 
    coupon_id: Optional[int], 
    coupon_value: Optional[int]
) -> int:
    """保存订单项"""
    status = 0
    try:
        with get_session(pkg) as session:
            order_item = WebStore(
                order_id=order_id,
                user_id=user_id,
                facebook_id=fb_id,
                create_ts=int(time.time()),
                price=price,
                coins=coins,
                coupon_id=coupon_id
            )
            
            if coupon_value:
                msg = {'coupon_value': coupon_value}
                order_item.ext = json.dumps(msg, separators=(',', ':'))
            
            session.add(order_item)
            session.commit()
            status = 1
            
    except Exception as e:
        if isinstance(e, IntegrityError):
            # 重复订单
            status = -1
        logger.error(f"save_order_item error: {e}")
    
    return status


def remove_inbox_coupon(pkg: str, user_id: int, coupon_id: int):
    """删除收件箱中的优惠券"""
    try:
        with get_session(pkg) as session:
            statement = (
                select(Inbox)
                .where(Inbox.id == coupon_id)
                .where(Inbox.user_id == user_id)
            )
            coupon = session.exec(statement).first()
            if coupon:
                session.delete(coupon)
                session.commit()
    except Exception as e:
        logger.error(f"remove_inbox_coupon error: {e}")


def utc2local(utc_dtm: datetime.datetime) -> datetime.datetime:
    """UTC时间转本地时间"""
    local_tm = datetime.datetime.fromtimestamp(0)
    utc_tm = datetime.datetime.utcfromtimestamp(0)
    offset = local_tm - utc_tm
    return utc_dtm + offset


def local2utc(local_dtm: datetime.datetime) -> datetime.datetime:
    """本地时间转UTC时间"""
    return datetime.datetime.utcfromtimestamp(local_dtm.timestamp())


def get_utc_ts_str(local_ts: datetime.datetime) -> str:
    """获取UTC时间戳字符串"""
    return local2utc(local_ts).strftime('%Y-%m-%d %H:%M:%S')


def send_reward_to_inbox(pkg: str, uid: int, tokens: int, reason: str = "购买奖励") -> bool:
    return True
    try:
        with get_session(pkg) as session:


            extra_data = { "attach_list": [[18, tokens, 1]]}
            
            count = 0
            valid_time_sec = -1  # -1表示永久有效
            inbox_type = 101  # 购买奖励类型
            msg = None
            resource = None
            now = datetime.datetime.now()
            
            # 创建收件箱记录
            inbox_record = Inbox(
                user_id=uid,
                type=inbox_type,
                count=count,
                ts=now,
                valid_time_sec=valid_time_sec,
                msg=msg,
                resource=resource,
                extra_data=json.dumps(extra_data) if extra_data is not None else None
            )
            
            # 创建收件箱日志记录
            inbox_log_record = InboxLog(
                user_id=uid,
                type=inbox_type,
                count=count,
                create_ts=now,
                gm_name="WebStore"
            )
            
            # 保存到数据库
            session.add(inbox_record)
            session.add(inbox_log_record)
            session.commit()
            
            logger.info(f"Successfully sent {tokens} tokens to user {uid} inbox, reason: {reason}")
            return True
            
    except Exception as e:
        logger.error(f"Failed to send reward to inbox - UID: {uid}, Tokens: {tokens}, Error: {str(e)}")
        return False
    