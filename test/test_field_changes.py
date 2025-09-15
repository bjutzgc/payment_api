#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单元测试：验证字段名变更后的功能
测试loginType -> login_type, loginId -> login_id, loginCode -> login_code, shareId -> share_id
测试UserBase中user_id -> uid的变更
"""
import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class TestFieldChanges:
    """测试字段变更的单元测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置"""
        # 获取测试token
        self.token = self._get_test_token()
    
    def _get_test_token(self) -> str:
        """获取测试用的token"""
        try:
            data = {"appId": "com.funtriolimited.slots.casino.free"}
            response = requests.post(f"{BASE_URL}/api/v1/token", json=data)
            if response.status_code == 200:
                return response.json().get("token", "")
        except:
            pass
        return ""
    
    def test_login_with_new_field_names(self):
        """测试使用新字段名的登录接口"""
        # 测试Facebook登录
        params = {
            "login_type": 1,
            "login_id": "facebook_test_123"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应包含新的字段名 uid（而不是user_id）
        assert "uid" in data or "status_code" in data
        if data.get("status_code") == 1:
            assert "uid" in data
            assert isinstance(data["uid"], str)
    
    def test_login_with_all_new_parameters(self):
        """测试所有新参数名的登录"""
        # 测试包含所有参数的登录
        params = {
            "login_type": 4,  # 邮箱登录
            "login_id": "test@example.com",
            "login_code": "123456",
            "share_id": "inviter_123"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证响应结构
        assert "status_code" in data
        assert "msg" in data
        
        # 如果登录成功，验证uid字段存在
        if data.get("status_code") == 1:
            assert "uid" in data
            assert "user_name" in data
            assert "level" in data
    
    def test_login_different_login_types(self):
        """测试不同登录类型的新字段名"""
        login_types = [
            (1, "facebook_123"),  # Facebook
            (2, "google_123"),    # Google  
            (3, "usertoken_123"), # UserToken
            (6, "apple_123")      # Apple
        ]
        
        for login_type, login_id in login_types:
            params = {
                "login_type": login_type,
                "login_id": login_id
            }
            response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
            
            assert response.status_code == 200, f"Login type {login_type} failed"
            data = response.json()
            assert "status_code" in data
            
            # 验证返回的字段使用新名称
            if data.get("status_code") == 1:
                assert "uid" in data
                assert "user_id" not in data  # 确保旧字段名不存在
    
    def test_login_with_optional_parameters(self):
        """测试可选参数share_id"""
        # 不提供share_id
        params = {
            "login_type": 1,
            "login_id": "test_no_share"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        assert response.status_code == 200
        
        # 提供share_id
        params = {
            "login_type": 1,
            "login_id": "test_with_share",
            "share_id": "inviter_456"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        assert response.status_code == 200
    
    def test_login_response_schema_validation(self):
        """验证登录响应的数据结构使用新字段名"""
        params = {
            "login_type": 1,
            "login_id": "schema_test_123"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证必需字段
        required_fields = ["status_code", "msg"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # 如果登录成功，验证用户相关字段
        if data.get("status_code") == 1:
            user_fields = ["uid", "user_name", "level"]
            for field in user_fields:
                assert field in data, f"Missing user field: {field}"
            
            # 验证字段类型
            assert isinstance(data["uid"], str)
            assert isinstance(data.get("user_name", ""), str)
            assert isinstance(data.get("level", 0), int)
    
    def test_error_handling_with_new_fields(self):
        """测试错误处理仍然正常工作"""
        # 测试缺少必需参数
        params = {
            "login_type": 1
            # 缺少login_id
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        # 应该返回422或400错误
        assert response.status_code in [400, 422]
        
        # 测试无效的login_type
        params = {
            "login_type": 999,  # 无效类型
            "login_id": "test123"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=params)
        assert response.status_code == 200
        data = response.json()
        assert data.get("status_code") == 0  # 应该返回失败
    
    def test_backward_compatibility_removed(self):
        """验证旧字段名不再被接受（确保完全迁移）"""
        # 使用旧字段名应该失败
        old_params = {
            "loginType": 1,
            "loginId": "old_field_test"
        }
        response = requests.get(f"{BASE_URL}/api/v1/login", params=old_params)
        # 应该返回422错误，因为缺少必需的新字段
        assert response.status_code == 422
    
    def test_test_route_uses_new_fields(self):
        """验证测试路由也使用新字段名"""
        response = requests.get(f"{BASE_URL}/test/login_test")
        
        if response.status_code == 200:
            data = response.json()
            # 验证测试路由返回的也是新字段名
            assert "uid" in data
            assert "user_id" not in data
        elif response.status_code == 403:
            # 生产环境下测试路由被禁用，这是正常的
            pass

def test_login_integration():
    """集成测试：完整的登录流程"""
    # 1. 获取token
    token_data = {"appId": "com.funtriolimited.slots.casino.free"}
    token_response = requests.post(f"{BASE_URL}/api/v1/token", json=token_data)
    assert token_response.status_code == 200
    token = token_response.json().get("token")
    
    # 2. 使用新字段名登录
    login_params = {
        "login_type": 1,
        "login_id": "integration_test_123",
        "share_id": "referrer_456"
    }
    login_response = requests.get(f"{BASE_URL}/api/v1/login", params=login_params)
    assert login_response.status_code == 200
    login_data = login_response.json()
    
    # 3. 验证返回使用新字段名
    if login_data.get("status_code") == 1:
        uid = login_data["uid"]
        assert isinstance(uid, str)
        
        # 4. 使用返回的uid进行后续API调用
        store_data = {"uid": uid}
        store_response = requests.post(f"{BASE_URL}/api/v1/store/items", json=store_data)
        assert store_response.status_code == 200

if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    test = TestFieldChanges()
    test.setup_method()
    
    print("开始测试字段变更...")
    
    try:
        test.test_login_with_new_field_names()
        print("✓ 新字段名登录测试通过")
        
        test.test_login_with_all_new_parameters()
        print("✓ 所有新参数测试通过")
        
        test.test_login_different_login_types()
        print("✓ 不同登录类型测试通过")
        
        test.test_login_response_schema_validation()
        print("✓ 响应结构验证通过")
        
        test.test_error_handling_with_new_fields()
        print("✓ 错误处理测试通过")
        
        test.test_backward_compatibility_removed()
        print("✓ 向后兼容性移除验证通过")
        
        print("所有字段变更测试通过！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()