# -*- coding: utf-8 -*-
"""
超简单的API测试
覆盖核心功能：token、登录、商城、每日奖励、支付成功/失败、历史订单
"""
import requests
import json

# 测试基础URL
BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    response = requests.get(f"{BASE_URL}/health")
    print("=== 健康检查 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_get_token():
    """测试获取token"""
    data = {"appId": "com.funtriolimited.slots.casino.free"}
    response = requests.post(f"{BASE_URL}/api/v1/token", json=data)
    print("=== 获取Token ===")
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {result}")
    token = result.get("token") if result.get("return_code") == 1 else None
    print(f"Token: {token}")
    print()
    return token

def test_login():
    """测试登录"""
    url = f"{BASE_URL}/api/v1/login?loginType=1&loginId=test123"
    response = requests.get(url)
    print("=== 登录测试 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_daily_gift():
    """测试每日奖励"""
    data = {"uid": "test123"}
    response = requests.post(f"{BASE_URL}/api/v1/daily_gift", json=data)
    print("=== 每日奖励 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_store_items():
    """测试商城信息"""
    data = {"uid": "test123"}
    response = requests.post(f"{BASE_URL}/api/v1/store/items", json=data)
    print("=== 商城信息 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_payment_success(token):
    """测试支付成功"""
    if not token:
        print("=== 支付成功 ===")
        print("错误: 没有token，跳过测试")
        print()
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "order_id": "test_order_001",
        "uid": "test123",
        "item_id": 1,
        "price": 19.99,
        "currency": "USD",
        "payment_channel": "stripe",
        "payment_method": "card",
        "ip": "127.0.0.1",
        "country": "US",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/api/v1/payment/success", json=data, headers=headers)
    print("=== 支付成功 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_payment_failure(token):
    """测试支付失败"""
    if not token:
        print("=== 支付失败 ===")
        print("错误: 没有token，跳过测试")
        print()
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "order_id": "test_order_002",
        "uid": "test123",
        "item_id": 1,
        "price": 19.99,
        "currency": "USD",
        "payment_channel": "stripe",
        "payment_method": "card",
        "ip": "127.0.0.1",
        "country": "US",
        "web_pay_error_code": "card_declined"
    }
    response = requests.post(f"{BASE_URL}/api/v1/payment/failure", json=data, headers=headers)
    print("=== 支付失败 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_order_history():
    """测试历史订单"""
    data = {"uid": "test123"}
    response = requests.post(f"{BASE_URL}/api/v1/orders/history", json=data)
    print("=== 历史订单 ===")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行超简单API测试")
    print("=" * 50)
    
    try:
        # 1. 健康检查
        test_health()
        
        # 2. 获取token
        token = test_get_token()
        
        # 3. 登录测试
        test_login()
        
        # 4. 每日奖励
        test_daily_gift()
        
        # 5. 商城信息
        test_store_items()
        
        # 6. 支付成功
        test_payment_success(token)
        
        # 7. 支付失败
        test_payment_failure(token)
        
        # 8. 历史订单
        test_order_history()
        
        print("✅ 所有测试完成!")
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")

if __name__ == "__main__":
    run_all_tests()