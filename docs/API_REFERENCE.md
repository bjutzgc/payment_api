# Payment API 接口参考文档

## 📋 接口列表

### 1. 认证接口
- [获取Token](#获取token) - `POST /api/v1/token`
- [用户登录](#用户登录) - `GET /api/v1/login`
- [刷新用户信息](#刷新用户信息) - `POST /api/v1/refresh`
- [每日礼物](#每日礼物) - `POST /api/v1/daily_gift`

### 2. 商城接口
- [获取商品列表](#获取商品列表) - `POST /api/v1/store/items`

### 3. 支付接口
- [支付成功回调](#支付成功回调) - `POST /api/v1/payment/success`
- [支付失败记录](#支付失败记录) - `POST /api/v1/payment/failure`

### 4. 订单接口
- [获取订单历史](#获取订单历史) - `POST /api/v1/orders/history`

---

## 🔐 认证接口

### 获取Token

**接口**: `POST /api/v1/token`

**请求参数**:
```json
{
  "appId": "com.funtriolimited.slots.casino.free"
}
```

**响应示例**:
```json
{
  "return_code": 1,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "msg": "Token获取成功"
}
```

### 用户登录

**接口**: `GET /api/v1/login`

**请求参数**:
- `login_type` (int, required): 登录类型
  - 1: Facebook登录
  - 2: Google登录
  - 3: UserToken登录
  - 4: 邮箱登录
  - 5: SMS登录
  - 6: Apple登录
- `login_id` (string, required): 登录ID
- `login_code` (string, optional): 验证码(邮箱/SMS登录时需要)
- `share_id` (string, optional): 邀请者ID

**响应示例**:
```json
{
  "status_code": 1,
  "uid": "12345",
  "user_name": "User_12345",
  "level": 1,
  "coins": "1000",
  "cash": "0",
  "daily_gift": 1,
  "avatar_url": "https://example.com/avatar.jpg",
  "msg": "登录成功",
  "show": 0
}
```

### 刷新用户信息

**接口**: `POST /api/v1/refresh`

**Headers**:
```
Authorization: Bearer {token}
```

**请求参数**:
```json
{
  "login_type": 1,
  "login_id": "user_id",
  "login_code": "123456",    // 验证码(邮箱/SMS登录时需要) - 可选
  "share_id": "inviter_id"   // 邀请者ID - 可选
}
```

**响应示例**:
```json
{
  "status_code": 1,
  "uid": "12345",
  "user_name": "User_12345",
  "level": 1,
  "coins": "1000",
  "cash": "0",
  "daily_gift": 1,
  "avatar_url": "https://example.com/avatar.jpg",
  "msg": "刷新成功",
  "show": 0
}
```

### 每日礼物

**接口**: `POST /api/v1/daily_gift`

**请求参数**:
```json
{
  "uid": "12345"
}
```

**响应示例**:
```json
{
  "return_code": 1
}
```

---

## 🛒 商城接口

### 获取商品列表

**接口**: `POST /api/v1/store/items`

**请求参数**:
```json
{
  "uid": "12345"
}
```

**响应示例**:
```json
{
  "return_code": 1,
  "is_first_pay": 1,
  "items": [
    {
      "id": 1,
      "default_price": 0.99,
      "tokens": 1000,
      "tokens_base": 1000,
      "bonus": 0.0,
      "act_items": []
    }
  ]
}
```

---

## 💰 支付接口

### 支付成功回调

**接口**: `POST /api/v1/payment/success`

**Headers**:
```
Authorization: Bearer {token}
```

**请求参数**:
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

**响应示例**:
```json
{
  "return_code": 1,
  "msg": "支付成功，奖励已发放！获得1000第三货币"
}
```

### 支付失败记录

**接口**: `POST /api/v1/payment/failure`

**Headers**:
```
Authorization: Bearer {token}
```

**请求参数**:
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

**响应示例**:
```json
{
  "return_code": 1,
  "msg": "支付失败记录已保存"
}
```

---

## 📦 订单接口

### 获取订单历史

**接口**: `POST /api/v1/orders/history`

**请求参数**:
```json
{
  "uid": "12345"
}
```

**响应示例**:
```json
{
  "status_code": 1,
  "data": [
    {
      "order_id": "order_12345",
      "item_name": "1000金币",
      "order_time": "2023-01-01 12:00:00",
      "order_status": "completed",
      "price": 0.99,
      "currency": "USD"
    }
  ]
}
```