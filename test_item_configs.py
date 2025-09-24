#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试商品配置模块
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from src.item_configs import (
    STORE_ITEMS_CONFIG, 
    get_item_name,
    get_available_store_items
)

def test_item_configs():
    """测试商品配置"""
    print("=== 测试商品配置 ===")
    
    # 检查STORE_ITEMS_CONFIG
    print("STORE_ITEMS_CONFIG 中的商品数量: {}".format(len(STORE_ITEMS_CONFIG)))
    for item in STORE_ITEMS_CONFIG:
        print("  ID: {}, Name: {}, Price: ${}".format(item['id'], item['name'], item['price']))
    
    print("\n=== 测试get_item_name ===")
    for i in range(1, 9):
        name = get_item_name(i)
        print("  商品 {} 名称: {}".format(i, name))
    
    print("\n=== 测试get_available_store_items ===")
    # 普通用户
    normal_items = get_available_store_items(5000, 50.0, False)
    print("普通用户可用商品数量: {}".format(len(normal_items)))
    
    # 高级用户
    high_level_items = get_available_store_items(15000, 100.0, False)
    print("高级用户可用商品数量: {}".format(len(high_level_items)))
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_item_configs()