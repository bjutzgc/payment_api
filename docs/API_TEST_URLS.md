# Payment API 测试URL集合

## 📋 目录
- [认证接口](#认证接口)
- [商城接口](#商城接口)
- [支付接口](#支付接口)
- [订单接口](#订单接口)
- [系统接口](#系统接口)
- [测试流程](#测试流程)

## 🔐 认证接口

### 获取Token
```
POST http://localhost:8000/api/v1/token
```

**请求体:**
```json
{
  "appId": "com.funtriolimited.slots.casino.free"
}
```

### 用户登录
```
GET http://localhost:8000/api/v1/login
```

**支持的登录类型:**
- `login_type=1`: Facebook登录，需要 `login_id` (Facebook ID)
- `login_type=2`: Google登录，需要 `login_id` (Google ID)
- `login_type=3`: UserToken登录，需要 `login_id` (任意值) + `user_token` (JWT Token)
- `login_type=4`: 邮箱登录，需要 `login_id` (邮箱地址) + `login_code` (验证码)
- `login_type=5`: SMS登录，需要 `login_id` (手机号) + `login_code` (验证码)
- `login_type=6`: Apple登录，需要 `login_id` (Apple ID)

**示例:**
```
GET http://localhost:8000/api/v1/login?login_type=1&login_id=facebook_test_id_12345
```

### 刷新用户信息
```
POST http://localhost:8000/api/v1/refresh
```

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**请求体:**
```json
{
  "login_type": 1,
  "login_id": "user_id",
  "login_code": "123456",    // 验证码(邮箱/SMS登录时需要) - 可选
  "share_id": "inviter_id"   // 邀请者ID - 可选
}
```

**示例:**
```bash
# 先获取token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 使用token刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "login_type": 1,
    "login_id": "facebook_test_id_12345"
  }'
```

### 每日礼物
```
POST http://localhost:8000/api/v1/daily_gift
```

**请求体:**
```json
{
  "uid": "12345"
}
```

## 🛒 商城接口

### 获取商品列表
```
POST http://localhost:8000/api/v1/store/items
```

**请求体:**
```json
{
  "uid": "12345"
}
```

## 💰 支付接口

### 支付成功回调
```
POST http://localhost:8000/api/v1/payment/success
```

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**请求体:**
```json
{
  "order_id": "order_12345",
  "uid": "12345",
  "item_id": 1,
  "price": 0.99,
  "currency": "USD",
  "payment_method": "card",
  "email": "user@example.com"
}
```

### 支付失败记录
```
POST http://localhost:8000/api/v1/payment/failure
```

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**请求体:**
```json
{
  "order_id": "order_12345",
  "uid": "12345",
  "item_id": 1,
  "web_pay_error_code": "CARD_DECLINED",
  "web_lang": "en",
  "browser_lang": "en-US",
  "payment_method": "card"
}
```

## 📦 订单接口

### 获取订单历史
```
POST http://localhost:8000/api/v1/orders/history
```

**请求体:**
```json
{
  "uid": "12345"
}
```

## ⚙️ 系统接口

### 健康检查
```
GET http://localhost:8000/health
```

### API文档
```
GET http://localhost:8000/docs     # Swagger UI
GET http://localhost:8000/redoc    # ReDoc
```

## 🔄 测试流程

### 1. 用户功能流程
```bash
# 1. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 2. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123"

# 3. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "login_type": 1,
    "login_id": "facebook_test_id_12345"
  }'

# 4. 获取商品列表
curl -X POST "http://localhost:8000/api/v1/store/items" \
  -H "Content-Type: application/json" \
  -d '{"uid": "10001"}'
```

### 2. 支付流程
```bash
# 1. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 2. 支付成功回调
curl -X POST "http://localhost:8000/api/v1/payment/success" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "order_id": "order_12345",
    "uid": "12345",
    "item_id": 1,
    "price": 0.99,
    "currency": "USD",
    "payment_method": "card",
    "email": "user@example.com"
  }'

# 3. 支付失败记录
curl -X POST "http://localhost:8000/api/v1/payment/failure" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "order_id": "order_12345",
    "uid": "12345",
    "item_id": 1,
    "web_pay_error_code": "CARD_DECLINED",
    "web_lang": "en",
    "browser_lang": "en-US",
    "payment_method": "card"
  }'
```