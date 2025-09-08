# Payment API 测试URL集合

本文件提供了Payment API的所有测试URL，方便开发者快速进行API测试。

## 🌐 基础信息
- **服务地址**: http://localhost:8000
- **API版本**: v1
- **测试环境**: 开发环境（DEBUG=True）

## 🏥 系统检查

### 健康检查
```
GET http://localhost:8000/health
```

### API文档
```
# Swagger UI
http://localhost:8000/docs

# ReDoc
http://localhost:8000/redoc
```

## 🧪 开发测试接口

### 基础测试
```
# 简单测试
GET http://localhost:8000/test/simple

# 连通性测试
GET http://localhost:8000/test/ping

# 数据库信息
GET http://localhost:8000/test/database_info
```

### 功能测试接口
```
# Token测试
GET http://localhost:8000/test/token_test

# 登录测试
GET http://localhost:8000/test/login_test

# 商城测试
GET http://localhost:8000/test/store_items_test

# 支付成功测试
GET http://localhost:8000/test/payment_success_test

# 支付失败测试
GET http://localhost:8000/test/payment_failure_test

# 订单历史测试
GET http://localhost:8000/test/order_history_test

# 每日礼物测试
GET http://localhost:8000/test/daily_gift_test
```

## 🔑 认证接口

### 获取Token
```
POST http://localhost:8000/api/v1/token
Content-Type: application/json

{
  "appId": "com.funtriolimited.slots.casino.free"
}
```

## 👤 用户接口

### Facebook登录
```
GET http://localhost:8000/api/v1/login?loginType=1&loginId=facebook123
```

### Google登录
```
GET http://localhost:8000/api/v1/login?loginType=2&loginId=google123
```

### Apple登录
```
GET http://localhost:8000/api/v1/login?loginType=6&loginId=apple123
```

### 邮箱登录
```
GET http://localhost:8000/api/v1/login?loginType=4&loginId=test@example.com&loginCode=123456
```

### SMS登录
```
GET http://localhost:8000/api/v1/login?loginType=5&loginId=13800138000&loginCode=123456
```

### 用户Token登录
```
GET http://localhost:8000/api/v1/login?loginType=3&loginId=usertoken123
```

## 🛒 商城接口

### 获取商品列表
```
POST http://localhost:8000/api/v1/store/items
Content-Type: application/json

{
  "uid": "10001"
}
```

### 每日礼物
```
POST http://localhost:8000/api/v1/daily_gift
Content-Type: application/json

{
  "uid": "10001"
}
```

## 💰 支付接口（需要Token认证）

### 支付成功 - 首充用户
```
POST http://localhost:8000/api/v1/payment/success
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN_HERE

{
  "order_id": "first_charge_001",
  "uid": "new_user_001",
  "item_id": 1,
  "price": 19.99,
  "currency": "USD",
  "payment_channel": "appcharge",
  "payment_method": "credit_card",
  "ip": "192.168.1.100",
  "country": "US",
  "email": "newuser@example.com"
}
```

### 支付成功 - 正常购买
```
POST http://localhost:8000/api/v1/payment/success
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN_HERE

{
  "order_id": "normal_purchase_001",
  "uid": "existing_user_001",
  "item_id": 2,
  "price": 29.99,
  "currency": "USD",
  "payment_channel": "appcharge",
  "payment_method": "paypal",
  "ip": "192.168.1.100",
  "country": "US",
  "email": "user@example.com"
}
```

### 支付失败
```
POST http://localhost:8000/api/v1/payment/failure
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN_HERE

{
  "order_id": "fail_order_001",
  "uid": "10001",
  "item_id": 1,
  "web_pay_error_code": "PAYMENT_CANCELLED",
  "web_lang": "zh-CN",
  "browser_lang": "zh",
  "payment_method": "credit_card"
}
```

## 📋 订单接口

### 订单历史
```
POST http://localhost:8000/api/v1/orders/history
Content-Type: application/json

{
  "uid": "10001"
}
```

## 🛠️ 完整测试流程

### 1. 基础验证流程
```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 简单测试
curl -X GET "http://localhost:8000/test/simple"

# 3. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'
```

### 2. 用户功能流程
```bash
# 1. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123"

# 2. 获取商品列表
curl -X POST "http://localhost:8000/api/v1/store/items" \
  -H "Content-Type: application/json" \
  -d '{"uid": "10001"}'

# 3. 每日礼物
curl -X POST "http://localhost:8000/api/v1/daily_gift" \
  -H "Content-Type: application/json" \
  -d '{"uid": "10001"}'
```

### 3. 支付功能流程（需要先获取Token）
```bash
# 1. 获取Token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}' | \
  grep -o '"token":"[^"]*"' | cut -d'"' -f4)

# 2. 支付成功
curl -X POST "http://localhost:8000/api/v1/payment/success" \
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
  }'

# 3. 订单历史
curl -X POST "http://localhost:8000/api/v1/orders/history" \
  -H "Content-Type: application/json" \
  -d '{"uid": "10001"}'
```

## 📊 商品ID参考

根据项目配置，以下是可用的商品ID：

| 商品ID | 商品名称 | 价格(USD) | 基础第三货币 | 首充奖励 |
|--------|----------|-----------|-------------|----------|
| 1 | 金币包 1000 | 19.99 | 20 | 22 |
| 2 | 金币包 2000 | 29.99 | 30 | 33 |
| 3 | 金币包 5000 | 49.99 | 50 | 55 |
| 4 | 金币包 10000 | 99.99 | 100 | 110 |
| 5 | 金币包 20000 | 199.99 | 200 | 220 |
| 6 | 金币包 40000 | 399.99 | 400 | 440 |
| 7 | 金币包 60000 | 599.99 | 600 | 660 |
| 8 | 金币包 100000 | 999.99 | 1000 | 1100 |

## 🚨 注意事项

### Token相关
- Token有效期为3小时
- 支付相关接口必须提供有效Token
- Token格式: `Bearer <token_string>`

### 测试数据
- 测试用户ID建议使用: 10001, 10002, 10003等
- 订单ID必须唯一，建议使用时间戳
- 邮箱地址使用测试邮箱，如: test@example.com

### 环境要求
- 服务必须在开发环境运行（DEBUG=True）
- Redis和数据库服务正常
- 端口8000可访问

### 错误处理
- HTTP 422: 参数验证错误
- HTTP 401: Token无效或过期
- HTTP 403: 测试接口在非开发环境不可用
- HTTP 500: 服务器内部错误

## 📁 Postman集合

可以将以上URL导入Postman创建测试集合：

1. 打开Postman
2. 创建新的Collection
3. 导入上述请求
4. 设置环境变量:
   - `base_url`: http://localhost:8000
   - `token`: 通过Token接口获取
   - `app_id`: com.funtriolimited.slots.casino.free

## 🔧 自动化测试脚本

项目提供了多个自动化测试脚本：

- `test_api_complete.py` - 完整API功能测试
- `test_purchase_success.py` - 购买成功流程测试
- `test_dynamic_store.py` - 动态商城测试
- `simple_test.py` - 基础功能测试

运行方式：
```bash
python test_api_complete.py
python test_purchase_success.py
```

---

> 📝 **提示**: 
> - 建议按照流程顺序进行测试
> - 首次使用建议先运行测试接口验证环境
> - 遇到问题请查看服务器日志
> - 更多详细信息请参考 [API测试文档](API_TESTING.md)