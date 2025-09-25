# -*- coding: utf-8 -*-

import time
from datetime import datetime, timezone
from authlib.jose import jwt, JoseError

# 配置参数
USER_TOKEN_SECRET_KEY = "oye9cVw6rJPb3AR512HjP_cEbuFKsC7_fHFdrimylnE"  # 生产环境使用强密码
USER_TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 24 * 60 * 30  # token有效期60分钟



def create_jwt_token(user_id: str) -> str:
    
    
    header = {'alg': USER_TOKEN_ALGORITHM}
    
    # 使用时间戳（Unix timestamp）
    now_ts = int(time.time())  # 当前时间戳（秒）
    expire_ts = now_ts + (TOKEN_EXPIRE_MINUTES * 60)  # 加上秒数
    
    payload = {
        'user_id': user_id,
        'iat': now_ts,  # 数字时间戳
        'exp': expire_ts,
        'iss': 'your-app-name',
        'aud': 'your-app-audience'
    }
    
    token = jwt.encode(header, payload, USER_TOKEN_SECRET_KEY)
    return token.decode('utf-8')


def verify_jwt_token(token: str):
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
                'error': 'Token已过期',
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
            'error': f'Token验证失败: {str(e)}'
        }


def get_user_id_from_token(token: str):
    """
    从JWT token中获取用户ID
    """
    payload = verify_jwt_token(token)
    if payload and 'success' in payload and payload['success']:
        return payload['user_id']
    return None

UIDS = [709, 703, 424, 389, 223, 220, 219, 217, 215, 214, 709, 10001]

for uid in UIDS:
    print(create_jwt_token(str(uid)))

