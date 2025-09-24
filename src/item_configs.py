# -*- coding: utf-8 -*-
"""
Item configuration module
Defines the mapping between item IDs and rewards
The number of store items is determined by user M (coins) >= 10000 and H (level) >= 99.99
"""
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

def calculate_tokens(base_tokens: int, bonus_rate: float, is_first_charge: bool = False) -> int:
    """
    Calculate the actual number of tokens to be issued
    
    Args:
        base_tokens: Base token count
        bonus_rate: Bonus rate (0.01 = 1%)
        is_first_charge: Whether this is the first charge
    
    Returns:
        int: Actual number of tokens to be issued
    """
    bonus_tokens = int(base_tokens * bonus_rate)
    return base_tokens + bonus_tokens


def is_high_level_user(user_coins: int, user_level: float) -> bool:
    """
    Determine if the user is a high-level user (M>=10000 and H>=99.99)
    
    Args:
        user_coins: User coin count (M)
        user_level: User level (H)
    
    Returns:
        bool: Whether the user is a high-level user
    """
    return user_coins >= 10000 and user_level >= 99.99


def get_available_store_items(user_coins: int, user_level: float, is_first_charge_user: bool = False) -> list:
    """
    Get the list of available store items for the user
    
    Args:
        user_coins: User coin count (M)
        user_level: User level (H)
        is_first_charge_user: Whether the user is a first-time charger
    
    Returns:
        list: Item list
    """
    # Determine the number of items based on user level
    if is_high_level_user(user_coins, user_level):
        # High-level user: 8 items
        available_items = STORE_ITEMS_CONFIG[2:]
    else:
        # Regular user: first 6 items
        available_items = STORE_ITEMS_CONFIG[2:]
    
    # Build the response data
    items = []
    for item in available_items:
        actual_tokens = calculate_tokens(item["base_tokens"], item["normal_bonus"] if not is_first_charge_user else item["first_bonus"])
            
        items.append({
            "id": item["id"],
            "name": item["name"],
            "price": item["price"],
            "tokens": actual_tokens,
            "base_tokens": item["base_tokens"],
            "bonus_rate": item["normal_bonus"] ,
            "first_rate": item["first_bonus"] if is_first_charge_user else 0.0,
            "act_items": []  # Additional items, can be configured as needed
        })
    
    return items


def get_item_config(item_id: int, user_coins: int = 0, user_level: float = 1.0, is_first_charge: bool = False) -> dict:
    """
    Get item configuration (dynamic version)
    
    Args:
        item_id: Item ID
        user_coins: User coin count
        user_level: User level
        is_first_charge: Whether this is the first charge
    
    Returns:
        dict: Item configuration, returns default configuration if not found
    """
    # First check the new configuration
    for item in STORE_ITEMS_CONFIG:
        if item["id"] == item_id:
            # Check if the user can access this item
            if item_id > 6 and not is_high_level_user(user_coins, user_level):
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


def get_item_tokens(item_id: int, user_coins: int = 0, user_level: float = 1.0, is_first_charge: bool = False) -> int:
    """
    Get the number of tokens for the item (dynamic version)
    
    Args:
        item_id: Item ID
        user_coins: User coin count
        user_level: User level
        is_first_charge: Whether this is the first charge
    
    Returns:
        int: Token count
    """
    config = get_item_config(item_id, user_coins, user_level, is_first_charge)
    return config["tokens"]


def get_item_name(item_id: int) -> str:
    """
    Get item name
    
    Args:
        item_id: Item ID
    
    Returns:
        str: Item name
    """
    # First check the new configuration
    for item in STORE_ITEMS_CONFIG:
        if item["id"] == item_id:
            return item["name"]
    
    return f"未知商品 {item_id}"


def get_all_items(user_coins: int = 0, user_level: float = 1.0, is_first_charge_user: bool = False) -> list:
    """
    Get all item configurations (for store interface)
    
    Args:
        user_coins: User coin count
        user_level: User level
        is_first_charge_user: Whether the user is a first-time charger
    
    Returns:
        list: List of all item configurations
    """
    return get_available_store_items(user_coins, user_level, is_first_charge_user)
