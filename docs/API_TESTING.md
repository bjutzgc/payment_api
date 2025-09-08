# Payment API 测试文档

## 📋 测试概述

本文档提供Payment API的完整测试指南，包括登录、商城、支付成功、支付失败、订单历史等核心功能的测试方法和示例。

## 🌐 测试环境信息

### 基础信息
- **测试基地址**: `http://localhost:8000`
- **API版本**: `v1`
- **认证方式**: JWT Bearer Token
- **内容类型**: `application/json`

### 环境要求
- 服务正常运行在端口8000
- Redis服务可用
- 数据库连接正常
- 开发环境（DEBUG=True）

## 🚀 快速开始测试

### 1. 健康检查
```bash
curl -X GET "http://localhost:8000/health"
```

**预期响应:**
```json
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 2. 访问API文档
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Token认证测试

### 获取Token
**接口**: `POST /api/v1/token`

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "com.funtriolimited.slots.casino.free"
  }'
```

**成功响应:**
```json
{
  "return_code": 1,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "msg": "Token获取成功"
}
```

**失败响应:**
```json
{
  "return_code": 0,
  "msg": "无效的AppId"
}
```

### Token测试接口
**接口**: `GET /test/token_test`

```bash
curl -X GET "http://localhost:8000/test/token_test"
```

## 👤 登录测试

### 登录接口
**接口**: `GET /api/v1/login`

**支持的登录类型:**
- 1: Facebook登录
- 2: Google登录  
- 3: UserToken登录
- 4: 邮箱登录（需要验证码）
- 5: SMS登录（需要验证码）
- 6: Apple ID登录

### Facebook登录测试
```bash
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=facebook123&shareId=invite456"
```

### Google登录测试
```bash
curl -X GET "http://localhost:8000/api/v1/login?loginType=2&loginId=google123"
```

### Apple登录测试
```bash
curl -X GET "http://localhost:8000/api/v1/login?loginType=6&loginId=apple123"
```

### 邮箱登录测试
```bash
curl -X GET "http://localhost:8000/api/v1/login?loginType=4&loginId=test@example.com&loginCode=123456"
```

**成功响应:**
```json
{
  "status_code": 1,
  "user_id": "12345",
  "user_name": "Test User",
  "level": 10,
  "daily_gift": 1,
  "avatar_url": "https://example.com/avatar.jpg",
  "msg": "登录成功"
}
```

**失败响应:**
```json
{
  "status_code": 0,
  "msg": "用户不存在"
}
```

### 登录测试接口
**接口**: `GET /test/login_test`

```bash
curl -X GET "http://localhost:8000/test/login_test"
```

## 🛒 商城商品测试

### 获取商品列表
**接口**: `POST /api/v1/store/items`

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/store/items" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "10001"
  }'
```

**成功响应:**
```json
{
  "return_code": 1,
  "is_first_pay": 1,
  "items": [
    {
      "id": 1,
      "name": "金币包 1000",
      "price": 19.99,
      "tokens": 22,
      "tokens_base": 20,
      "bonus": 10,
      "act_items": [
        {
          "id": 100,
          "name": "金币包",
          "num": 10
        }
      ]
    },
    {
      "id": 2,
      "name": "金币包 2000",
      "price": 29.99,
      "tokens": 33,
      "tokens_base": 30,
      "bonus": 10,
      "act_items": []
    }
  ]
}
```

### 商城测试接口
**接口**: `GET /test/store_items_test`

```bash
curl -X GET "http://localhost:8000/test/store_items_test"
```

### 测试说明
- `is_first_pay`: 1表示首充用户，0表示非首充用户
- `tokens`: 实际获得的第三货币数量
- `tokens_base`: 基础第三货币数量
- `bonus`: 奖励百分比
- `act_items`: 附加奖励商品

## 💰 支付成功测试

### 支付成功接口
**接口**: `POST /api/v1/payment/success`

**认证要求**: 需要Bearer Token

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/payment/success" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "order_id": "order_20250908_001",
    "uid": "10001",
    "item_id": 1,
    "price": 19.99,
    "currency": "USD",
    "payment_channel": "appcharge",
    "payment_method": "credit_card",
    "ip": "192.168.1.100",
    "country": "US",
    "email": "test@example.com"
  }'
```

**首充成功响应:**
```json
{
  "return_code": 1,
  "msg": "支付成功，奖励已发放！获得22第三货币(首充奖励)"
}
```

**正常购买成功响应:**
```json
{
  "return_code": 1,
  "msg": "支付成功，奖励已发放！获得20第三货币"
}
```

**失败响应:**
```json
{
  "return_code": 0,
  "err_code": 500,
  "msg": "处理失败: 错误信息"
}
```

### 支付成功测试接口
**接口**: `GET /test/payment_success_test`

```bash
curl -X GET "http://localhost:8000/test/payment_success_test"
```

### 测试场景

#### 1. 首充用户测试
```bash
# 获取Token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}' | \
  grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 首充支付测试
curl -X POST "http://localhost:8000/api/v1/payment/success" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "order_id": "first_charge_001",
    "uid": "new_user_001",
    "item_id": 1,
    "price": 19.99,
    "currency": "USD",
    "payment_channel": "appcharge",
    "payment_method": "credit_card",
    "email": "newuser@example.com"
  }'
```

#### 2. 正常购买测试
```bash
curl -X POST "http://localhost:8000/api/v1/payment/success" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "order_id": "normal_purchase_001",
    "uid": "existing_user_001",
    "item_id": 2,
    "price": 29.99,
    "currency": "USD",
    "payment_channel": "appcharge",
    "payment_method": "paypal",
    "email": "user@example.com"
  }'
```

## ❌ 支付失败测试

### 支付失败接口
**接口**: `POST /api/v1/payment/failure`

**认证要求**: 需要Bearer Token

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/payment/failure" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "order_id": "fail_order_001",
    "uid": "10001",
    "item_id": 1,
    "web_pay_error_code": "PAYMENT_CANCELLED",
    "web_lang": "zh-CN",
    "browser_lang": "zh",
    "payment_method": "credit_card"
  }'
```

**成功记录响应:**
```json
{
  "return_code": 1,
  "msg": "支付失败记录已保存"
}
```

**记录失败响应:**
```json
{
  "return_code": 0,
  "err_code": 500,
  "msg": "记录失败: 错误信息"
}
```

### 支付失败测试接口
**接口**: `GET /test/payment_failure_test`

```bash
curl -X GET "http://localhost:8000/test/payment_failure_test"
```

### 常见失败错误码
- `PAYMENT_CANCELLED`: 用户取消支付
- `PAYMENT_FAILED`: 支付失败
- `INSUFFICIENT_FUNDS`: 余额不足
- `NETWORK_ERROR`: 网络错误
- `TIMEOUT`: 支付超时

## 📋 订单历史测试

### 获取订单历史
**接口**: `POST /api/v1/orders/history`

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/orders/history" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "10001"
  }'
```

**成功响应:**
```json
{
  "status_code": 1,
  "data": [
    {
      "order_id": "order_20250908_001",
      "item_name": "金币包 1000",
      "order_time": "2025-09-08 16:30:00",
      "order_status": "completed",
      "price": 19.99,
      "currency": "USD"
    },
    {
      "order_id": "order_20250907_002",
      "item_name": "钻石包 500",
      "order_time": "2025-09-07 14:20:00",
      "order_status": "completed",
      "price": 29.99,
      "currency": "USD"
    }
  ],
  "msg": null
}
```

### 订单历史测试接口
**接口**: `GET /test/order_history_test`

```bash
curl -X GET "http://localhost:8000/test/order_history_test"
```

### 订单状态说明
- `completed`: 已完成
- `failed`: 失败
- `pending`: 待处理
- `cancelled`: 已取消

## 🎁 每日礼物测试

### 领取每日礼物
**接口**: `POST /api/v1/daily_gift`

**请求示例:**
```bash
curl -X POST "http://localhost:8000/api/v1/daily_gift" \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "10001"
  }'
```

**成功响应:**
```json
{
  "return_code": 1,
  "msg": null
}
```

### 每日礼物测试接口
**接口**: `GET /test/daily_gift_test`

```bash
curl -X GET "http://localhost:8000/test/daily_gift_test"
```

## 🧪 开发测试接口

### 简单测试
**接口**: `GET /test/simple`

```bash
curl -X GET "http://localhost:8000/test/simple"
```

**响应:**
```json
{
  "message": "Payment API Test Router is working",
  "status": "ok",
  "timestamp": "2025-09-04"
}
```

### 连通性测试
**接口**: `GET /test/ping`

```bash
curl -X GET "http://localhost:8000/test/ping"
```

**响应:**
```json
{
  "ping": "pong"
}
```

### 数据库信息测试
**接口**: `GET /test/database_info`

```bash
curl -X GET "http://localhost:8000/test/database_info"
```

## 📝 完整测试脚本

### Python测试脚本
```python
#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000"
APP_ID = "com.funtriolimited.slots.casino.free"

def get_token():
    """获取访问Token"""
    url = f"{BASE_URL}/api/v1/token"
    data = {"appId": APP_ID}
    response = requests.post(url, json=data)
    result = response.json()
    return result.get("token") if result.get("return_code") == 1 else None

def test_complete_flow():
    """完整测试流程"""
    # 1. 健康检查
    health = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {health.json()}")
    
    # 2. 获取Token
    token = get_token()
    if not token:
        print("Failed to get token")
        return
    print(f"Token: {token[:20]}...")
    
    # 3. 测试登录
    login_resp = requests.get(f"{BASE_URL}/api/v1/login?loginType=1&loginId=test123")
    print(f"Login: {login_resp.json()}")
    
    # 4. 测试商城
    store_resp = requests.post(f"{BASE_URL}/api/v1/store/items", 
                              json={"uid": "10001"})
    print(f"Store: {store_resp.json()}")
    
    # 5. 测试支付成功
    headers = {"Authorization": f"Bearer {token}"}
    payment_data = {
        "order_id": "test_order_001",
        "uid": "10001",
        "item_id": 1,
        "price": 19.99,
        "currency": "USD",
        "payment_channel": "appcharge",
        "payment_method": "credit_card",
        "email": "test@example.com"
    }
    payment_resp = requests.post(f"{BASE_URL}/api/v1/payment/success",
                                json=payment_data, headers=headers)
    print(f"Payment Success: {payment_resp.json()}")
    
    # 6. 测试订单历史
    history_resp = requests.post(f"{BASE_URL}/api/v1/orders/history",
                                json={"uid": "10001"})
    print(f"Order History: {history_resp.json()}")

if __name__ == "__main__":
    test_complete_flow()
```

### Bash测试脚本
```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
APP_ID="com.funtriolimited.slots.casino.free"

echo "🚀 开始Payment API测试"

# 1. 健康检查
echo "1️⃣ 健康检查..."
curl -s -X GET "$BASE_URL/health" | jq .

# 2. 获取Token
echo "2️⃣ 获取Token..."
TOKEN=$(curl -s -X POST "$BASE_URL/api/v1/token" \
  -H "Content-Type: application/json" \
  -d "{\"appId\": \"$APP_ID\"}" | \
  jq -r '.token')

if [ "$TOKEN" = "null" ]; then
  echo "❌ Token获取失败"
  exit 1
fi
echo "✅ Token获取成功: ${TOKEN:0:20}..."

# 3. 测试登录
echo "3️⃣ 测试登录..."
curl -s -X GET "$BASE_URL/api/v1/login?loginType=1&loginId=test123" | jq .

# 4. 测试商城
echo "4️⃣ 测试商城..."
curl -s -X POST "$BASE_URL/api/v1/store/items" \
  -H "Content-Type: application/json" \
  -d '{"uid": "10001"}' | jq .

# 5. 测试支付成功
echo "5️⃣ 测试支付成功..."
curl -s -X POST "$BASE_URL/api/v1/payment/success" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "order_id": "test_order_001",
    "uid": "10001",
    "item_id": 1,
    "price": 19.99,
    "currency": "USD",
    "payment_channel": "appcharge", 
    "payment_method": "credit_card",
    "email": "test@example.com"
  }' | jq .

echo "🎉 测试完成"
```

## ⚡ 推荐测试顺序

1. **基础连通性测试**
   - 健康检查: `GET /health`
   - 简单测试: `GET /test/simple`
   - 连通性测试: `GET /test/ping`

2. **认证测试**
   - Token获取: `POST /api/v1/token`
   - Token测试: `GET /test/token_test`

3. **业务功能测试**
   - 登录测试: `GET /api/v1/login`
   - 商城测试: `POST /api/v1/store/items`
   - 支付成功: `POST /api/v1/payment/success`
   - 支付失败: `POST /api/v1/payment/failure`
   - 订单历史: `POST /api/v1/orders/history`

4. **完整流程测试**
   - 首充用户完整购买流程
   - 老用户正常购买流程
   - 错误场景处理测试

## 🚨 常见问题

### Token相关
- **问题**: 401 Unauthorized
- **解决**: 检查Token是否正确，是否在Header中正确设置Authorization

### 参数验证
- **问题**: 422 Validation Error
- **解决**: 检查请求参数是否完整和格式正确

### 服务连接
- **问题**: Connection Error
- **解决**: 确认服务运行状态，检查端口和网络连接

### 环境配置
- **问题**: 测试接口403 Forbidden
- **解决**: 确认在开发环境（DEBUG=True）中运行

---

> 📝 **注意**: 
> - 测试接口仅在开发环境（DEBUG=True）中可用
> - 生产环境请使用实际业务接口
> - 请替换示例中的Token和参数为实际值
> 
> 🔗 **相关文档**: 
> - 参考 `docs/PROJECT_STRUCTURE.md` 了解项目结构
> - 查看 `src/routers/payment_routes.py` 了解接口实现