# -*- coding: utf-8 -*-
"""
pytest版本的超简单API测试
运行: pytest test/test_api.py -v
"""
import requests
import pytest

BASE_URL = "http://localhost:8000"
TEST_UID = "test123"
TEST_APP_ID = "com.funtriolimited.slots.casino.free"

class TestPaymentAPI:
    """Payment API 测试类"""
    
    def test_health_check(self):
        """测试健康检查"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_get_token(self):
        """测试获取token"""
        data = {"appId": TEST_APP_ID}
        response = requests.post(f"{BASE_URL}/api/v1/token", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["return_code"] == 1
        assert "token" in result
        return result["token"]
    
    def test_login(self):
        """测试登录"""
        url = f"{BASE_URL}/api/v1/login?loginType=1&loginId={TEST_UID}"
        response = requests.get(url)
        assert response.status_code == 200
        # 注意：登录可能失败（用户不存在），这里只测试接口可达性
    
    def test_daily_gift(self):
        """测试每日奖励"""
        data = {"uid": TEST_UID}
        response = requests.post(f"{BASE_URL}/api/v1/daily_gift", json=data)
        assert response.status_code == 200
        result = response.json()
        assert "return_code" in result
    
    def test_store_items(self):
        """测试商城信息"""
        data = {"uid": TEST_UID}
        response = requests.post(f"{BASE_URL}/api/v1/store/items", json=data)
        assert response.status_code == 200
        result = response.json()
        assert "return_code" in result
        assert "items" in result
    
    def test_payment_success(self):
        """测试支付成功"""
        # 先获取token
        token_data = {"appId": TEST_APP_ID}
        token_response = requests.post(f"{BASE_URL}/api/v1/token", json=token_data)
        token = token_response.json().get("token")
        
        if not token:
            pytest.skip("无法获取token")
        
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "order_id": "test_order_001",
            "uid": TEST_UID,
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
        assert response.status_code == 200
        result = response.json()
        assert "return_code" in result
    
    def test_payment_failure(self):
        """测试支付失败"""
        # 先获取token
        token_data = {"appId": TEST_APP_ID}
        token_response = requests.post(f"{BASE_URL}/api/v1/token", json=token_data)
        token = token_response.json().get("token")
        
        if not token:
            pytest.skip("无法获取token")
        
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "order_id": "test_order_002",
            "uid": TEST_UID,
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
        assert response.status_code == 200
        result = response.json()
        assert "return_code" in result
    
    def test_order_history(self):
        """测试历史订单"""
        data = {"uid": TEST_UID}
        response = requests.post(f"{BASE_URL}/api/v1/orders/history", json=data)
        assert response.status_code == 200
        result = response.json()
        assert "status_code" in result
        assert "data" in result

if __name__ == "__main__":
    # 直接运行测试
    import sys
    import subprocess
    subprocess.run([sys.executable, "-m", "pytest", __file__, "-v"])