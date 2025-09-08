# -*- coding: utf-8 -*-
"""
商品配置模块
定义商品ID与奖励的对应关系
根据用户M(金币)>=10000且H(等级)>=99.99决定商店商品数量
"""

# 商店商品基础配置
STORE_ITEMS_CONFIG = [
    {
        "id": 1,
        "price": 19.99,
        "name": "入门礼包",
        "description": "新手推荐礼包",
        "normal_bonus": 0,      # 正常促销比例
        "first_charge_bonus": 0.1,  # 首充促销比例
        "base_tokens": 20       # 基础第三货币数量
    },
    {
        "id": 2,
        "price": 29.99,
        "name": "成长礼包",
        "description": "热门推荐礼包",
        "normal_bonus": 0,
        "first_charge_bonus": 0.1,
        "base_tokens": 30
    },
    {
        "id": 3,
        "price": 49.99,
        "name": "进阶礼包",
        "description": "进阶玩家礼包",
        "normal_bonus": 0,
        "first_charge_bonus": 0.1,
        "base_tokens": 50
    },
    {
        "id": 4,
        "price": 99.99,
        "name": "精英礼包",
        "description": "精英玩家礼包",
        "normal_bonus": 0.01,
        "first_charge_bonus": 0.15,
        "base_tokens": 100
    },
    {
        "id": 5,
        "price": 199.99,
        "name": "豪华礼包",
        "description": "豪华玩家礼包",
        "normal_bonus": 0.02,
        "first_charge_bonus": 0.15,
        "base_tokens": 200
    },
    {
        "id": 6,
        "price": 399.99,
        "name": "至尊礼包",
        "description": "至尊玩家礼包",
        "normal_bonus": 0.04,
        "first_charge_bonus": 0.25,
        "base_tokens": 400
    },
    {
        "id": 7,
        "price": 599.99,
        "name": "传奇礼包",
        "description": "传奇玩家礼包",
        "normal_bonus": 0.05,
        "first_charge_bonus": 0.25,
        "base_tokens": 600
    },
    {
        "id": 8,
        "price": 999.99,
        "name": "神话礼包",
        "description": "神话级玩家礼包",
        "normal_bonus": 0.06,
        "first_charge_bonus": 0.25,
        "base_tokens": 1000
    }
]

# 旧版商品配置字典（保持向后兼容）
ITEM_CONFIGS = {
    1: {
        "name": "入门礼包",
        "tokens": 22,  # 首充奖励
        "base_tokens": 20,
        "bonus_percent": 10,
        "description": "新手推荐礼包"
    },
    2: {
        "name": "成长礼包",
        "tokens": 33,
        "base_tokens": 30,
        "bonus_percent": 10,
        "description": "热门推荐礼包"
    },
    3: {
        "name": "进阶礼包",
        "tokens": 55,
        "base_tokens": 50,
        "bonus_percent": 10,
        "description": "进阶玩家礼包"
    },
    4: {
        "name": "精英礼包",
        "tokens": 115,
        "base_tokens": 100,
        "bonus_percent": 15,
        "description": "精英玩家礼包"
    },
    5: {
        "name": "豪华礼包",
        "tokens": 230,
        "base_tokens": 200,
        "bonus_percent": 15,
        "description": "豪华玩家礼包"
    },
    6: {
        "name": "至尊礼包",
        "tokens": 500,
        "base_tokens": 400,
        "bonus_percent": 25,
        "description": "至尊玩家礼包"
    },
    7: {
        "name": "传奇礼包",
        "tokens": 750,
        "base_tokens": 600,
        "bonus_percent": 25,
        "description": "传奇玩家礼包"
    },
    8: {
        "name": "神话礼包",
        "tokens": 1250,
        "base_tokens": 1000,
        "bonus_percent": 25,
        "description": "神话级玩家礼包"
    }
}


def calculate_tokens(base_tokens: int, bonus_rate: float, is_first_charge: bool = False) -> int:
    """
    计算实际发放的第三货币数量
    
    Args:
        base_tokens: 基础第三货币数量
        bonus_rate: 奖励比例 (0.01 = 1%)
        is_first_charge: 是否首充
    
    Returns:
        int: 实际发放的第三货币数量
    """
    bonus_tokens = int(base_tokens * bonus_rate)
    return base_tokens + bonus_tokens


def is_high_level_user(user_coins: int, user_level: float) -> bool:
    """
    判断是否为高级用户（M>=10000且H>=99.99）
    
    Args:
        user_coins: 用户金币数量 (M)
        user_level: 用户等级 (H)
    
    Returns:
        bool: 是否为高级用户
    """
    return user_coins >= 10000 and user_level >= 99.99


def get_available_store_items(user_coins: int, user_level: float, is_first_charge_user: bool = False) -> list:
    """
    获取用户可用的商店商品列表
    
    Args:
        user_coins: 用户金币数量 (M)
        user_level: 用户等级 (H)
        is_first_charge_user: 是否为首充用户
    
    Returns:
        list: 商品列表
    """
    # 判断用户等级决定商品数量
    if is_high_level_user(user_coins, user_level):
        # 高级用户：8项商品
        available_items = STORE_ITEMS_CONFIG[:8]
    else:
        # 普通用户：前6项商品
        available_items = STORE_ITEMS_CONFIG[:6]
    
    # 构建返回数据
    items = []
    for item in available_items:
        # 选择促销比例
        bonus_rate = item["first_charge_bonus"] if is_first_charge_user else item["normal_bonus"]
        
        # 计算实际奖励
        actual_tokens = calculate_tokens(item["base_tokens"], bonus_rate, is_first_charge_user)
        
        items.append({
            "id": item["id"],
            "name": item["name"],
            "price": item["price"],
            "tokens": actual_tokens,
            "base_tokens": item["base_tokens"],
            "bonus_rate": bonus_rate,
            "bonus_percent": int(bonus_rate * 100),
            "description": item["description"],
            "is_first_charge": is_first_charge_user,
            "act_items": []  # 附加商品，可以根据需要配置
        })
    
    return items


def get_item_config(item_id: int, user_coins: int = 0, user_level: float = 1.0, is_first_charge: bool = False) -> dict:
    """
    获取商品配置（动态版本）
    
    Args:
        item_id: 商品ID
        user_coins: 用户金币数量
        user_level: 用户等级
        is_first_charge: 是否首充
    
    Returns:
        dict: 商品配置，如果不存在返回默认配置
    """
    # 先检查新版配置
    for item in STORE_ITEMS_CONFIG:
        if item["id"] == item_id:
            # 检查用户是否能访问该商品
            if item_id > 6 and not is_high_level_user(user_coins, user_level):
                # 普通用户不能访问7-8号商品
                return {
                    "name": f"不可用商品 {item_id}",
                    "tokens": 0,
                    "base_tokens": 0,
                    "bonus_percent": 0,
                    "description": "该商品仅对高级用户开放"
                }
            
            # 选择促销比例
            bonus_rate = item["first_charge_bonus"] if is_first_charge else item["normal_bonus"]
            actual_tokens = calculate_tokens(item["base_tokens"], bonus_rate, is_first_charge)
            
            return {
                "name": item["name"],
                "tokens": actual_tokens,
                "base_tokens": item["base_tokens"],
                "bonus_percent": int(bonus_rate * 100),
                "description": item["description"]
            }
    
    # 如果新版配置中没有，检查旧版配置（向后兼容）
    if item_id in ITEM_CONFIGS:
        return ITEM_CONFIGS[item_id]
    
    # 默认配置
    return {
        "name": f"未知商品 {item_id}",
        "tokens": 100,  # 默认给100第三货币
        "base_tokens": 100,
        "bonus_percent": 0,
        "description": "未知商品"
    }


def get_item_tokens(item_id: int, user_coins: int = 0, user_level: float = 1.0, is_first_charge: bool = False) -> int:
    """
    获取商品的第三货币奖励数量（动态版本）
    
    Args:
        item_id: 商品ID
        user_coins: 用户金币数量
        user_level: 用户等级
        is_first_charge: 是否首充
    
    Returns:
        int: 第三货币数量
    """
    config = get_item_config(item_id, user_coins, user_level, is_first_charge)
    return config["tokens"]


def get_item_name(item_id: int) -> str:
    """
    获取商品名称
    
    Args:
        item_id: 商品ID
    
    Returns:
        str: 商品名称
    """
    # 先检查新版配置
    for item in STORE_ITEMS_CONFIG:
        if item["id"] == item_id:
            return item["name"]
    
    # 如果新版配置中没有，检查旧版配置
    if item_id in ITEM_CONFIGS:
        return ITEM_CONFIGS[item_id]["name"]
    
    return f"未知商品 {item_id}"


def get_all_items(user_coins: int = 0, user_level: float = 1.0, is_first_charge_user: bool = False) -> list:
    """
    获取所有商品配置（用于商城接口）
    
    Args:
        user_coins: 用户金币数量
        user_level: 用户等级
        is_first_charge_user: 是否为首充用户
    
    Returns:
        list: 所有商品的配置列表
    """
    return get_available_store_items(user_coins, user_level, is_first_charge_user)


# 兼容性函数：旧版本的 get_item_tokens 和 get_item_config
def get_item_tokens_legacy(item_id: int) -> int:
    """
    获取商品的金币奖励数量（旧版兼容）
    
    Args:
        item_id: 商品ID
    
    Returns:
        int: 金币数量
    """
    if item_id in ITEM_CONFIGS:
        return ITEM_CONFIGS[item_id]["tokens"]
    return 100  # 默认值


def get_item_config_legacy(item_id: int) -> dict:
    """
    获取商品配置（旧版兼容）
    
    Args:
        item_id: 商品ID
    
    Returns:
        dict: 商品配置，如果不存在返回默认配置
    """
    return ITEM_CONFIGS.get(item_id, {
        "name": f"未知商品 {item_id}",
        "tokens": 100,  # 默认给100金币
        "base_tokens": 100,
        "bonus_percent": 0,
        "description": "未知商品"
    })