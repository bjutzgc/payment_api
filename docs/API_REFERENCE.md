# Payment API 接口参考文档

## 📋 API概述

Payment API 提供完整的支付系统功能，包括用户认证、商城管理、支付处理、订单管理等核心功能。所有API遵循RESTful设计原则，使用JSON格式进行数据交换。

## 🌐 基础信息

- **基础URL**: `http://localhost:8000` (开发环境)
- **API版本**: `v1`
- **认证方式**: JWT Bearer Token
- **内容类型**: `application/json`
- **字符编码**: `UTF-8`

## 🔑 认证机制

### JWT Token认证
大部分API接口需要在请求头中包含有效的JWT Token：

```http
Authorization: Bearer <your_jwt_token>
```

### Token获取流程
1. 调用 `/api/v1/token` 接口获取Token
2. Token有效期为3小时
3. 在后续API请求中使用Token进行认证

## 📚 接口分类

### 1. 认证接口
- [获取Token](#获取token) - `POST /api/v1/token`

### 2. 用户接口
- [用户登录](#用户登录) - `GET /api/v1/login`
- [每日礼物](#每日礼物) - `POST /api/v1/daily_gift`

### 3. 商城接口
- [获取商品列表](#获取商品列表) - `POST /api/v1/store/items`

### 4. 支付接口
- [支付成功](#支付成功) - `POST /api/v1/payment/success`
- [支付失败](#支付失败) - `POST /api/v1/payment/failure`

### 5. 订单接口
- [订单历史](#订单历史) - `POST /api/v1/orders/history`

### 6. 系统接口
- [健康检查](#健康检查) - `GET /health`

### 7. 测试接口（开发环境）
- [测试接口列表](#测试接口)

---

## 🔐 认证接口

### 获取Token

获取用于API认证的JWT Token。

**接口地址**: `POST /api/v1/token`

**请求参数**:
```json
{
  "appId": "com.funtriolimited.slots.casino.free"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appId | string | 是 | 应用程序ID |

**成功响应**:
```json
{
  "return_code": 1,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "msg": "Token获取成功"
}
```

**失败响应**:
```json
{
  "return_code": 0,
  "msg": "无效的AppId"
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| return_code | int | 返回码：1=成功，0=失败 |
| token | string | JWT Token（成功时返回） |
| msg | string | 响应消息 |

**示例代码**:
```bash
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'
```

---

## 👤 用户接口

### 用户登录

支持多种登录方式的用户登录接口。

**接口地址**: `GET /api/v1/login`

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| loginType | int | 是 | 登录类型：1=Facebook, 2=Google, 3=UserToken, 4=Email, 5=SMS, 6=Apple |
| loginId | string | 是 | 登录ID |
| loginCode | string | 否 | 验证码（邮箱/SMS登录时必填） |
| shareId | string | 否 | 邀请者ID |

**登录类型说明**:
- `1`: Facebook登录 - 需要Facebook ID
- `2`: Google登录 - 需要Google ID
- `3`: UserToken登录 - 需要用户Token
- `4`: Email登录 - 需要邮箱地址和验证码
- `5`: SMS登录 - 需要手机号和验证码
- `6`: Apple登录 - 需要Apple ID

**成功响应**:
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

**失败响应**:
```json
{
  "status_code": 0,
  "msg": "用户不存在"
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| status_code | int | 状态码：1=成功，0=失败 |
| user_id | string | 用户ID |
| user_name | string | 用户名 |
| level | int | 用户等级 |
| daily_gift | int | 每日礼物状态：0=不可领取，1=可领取 |
| avatar_url | string | 头像URL |
| msg | string | 响应消息 |

**示例代码**:
```bash
# Facebook登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=facebook123"

# Google登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=2&loginId=google123"

# Email登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=4&loginId=user@example.com&loginCode=123456"
```

### 每日礼物

领取每日奖励接口。

**接口地址**: `POST /api/v1/daily_gift`

**请求参数**:
```json
{
  "uid": "12345"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uid | string | 是 | 用户ID |

**成功响应**:
```json
{
  "return_code": 1
}
```

**失败响应**:
```json
{
  "return_code": 0,
  "err_code": 999
}
```

---

## 🛒 商城接口

### 获取商品列表

获取用户可购买的商品列表，支持动态商品配置。

**接口地址**: `POST /api/v1/store/items`

**请求参数**:
```json
{
  "uid": "12345"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uid | string | 是 | 用户ID |

**成功响应**:
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

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| return_code | int | 返回码：1=成功，0=失败 |
| is_first_pay | int | 是否首充用户：1=是，0=否 |
| items | array | 商品列表 |

**商品字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 商品ID |
| name | string | 商品名称 |
| price | float | 价格（美元） |
| tokens | int | 实际获得的第三货币数量 |
| tokens_base | int | 基础第三货币数量 |
| bonus | int | 奖励百分比 |
| act_items | array | 附加奖励商品 |

**示例代码**:
```bash
curl -X POST "http://localhost:8000/api/v1/store/items" \
  -H "Content-Type: application/json" \
  -d '{"uid": "12345"}'
```

---

## 💰 支付接口

### 支付成功

处理支付成功的回调接口。

**接口地址**: `POST /api/v1/payment/success`

**认证要求**: 需要Bearer Token

**请求参数**:
```json
{
  "order_id": "order_20250908_001",
  "uid": "12345",
  "item_id": 1,
  "price": 19.99,
  "currency": "USD",
  "payment_channel": "appcharge",
  "payment_method": "credit_card",
  "ip": "192.168.1.100",
  "country": "US",
  "email": "user@example.com"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | string | 是 | 订单ID（唯一） |
| uid | string | 是 | 用户ID |
| item_id | int | 是 | 商品ID |
| price | float | 是 | 支付金额 |
| currency | string | 是 | 货币类型（如USD） |
| payment_channel | string | 否 | 支付渠道 |
| payment_method | string | 否 | 支付方式 |
| ip | string | 否 | 用户IP地址 |
| country | string | 否 | 用户国家 |
| email | string | 否 | 用户邮箱 |

**成功响应**:
```json
{
  "return_code": 1,
  "msg": "支付成功，奖励已发放！获得22第三货币(首充奖励)"
}
```

**失败响应**:
```json
{
  "return_code": 0,
  "err_code": 500,
  "msg": "处理失败: 错误信息"
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| return_code | int | 返回码：1=成功，0=失败 |
| err_code | int | 错误码（失败时返回） |
| msg | string | 响应消息 |

**示例代码**:
```bash
curl -X POST "http://localhost:8000/api/v1/payment/success" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "order_id": "order_20250908_001",
    "uid": "12345",
    "item_id": 1,
    "price": 19.99,
    "currency": "USD",
    "payment_channel": "appcharge",
    "payment_method": "credit_card",
    "email": "user@example.com"
  }'
```

### 支付失败

记录支付失败信息的接口。

**接口地址**: `POST /api/v1/payment/failure`

**认证要求**: 需要Bearer Token

**请求参数**:
```json
{
  "order_id": "fail_order_001",
  "uid": "12345",
  "item_id": 1,
  "web_pay_error_code": "PAYMENT_CANCELLED",
  "web_lang": "zh-CN",
  "browser_lang": "zh",
  "payment_method": "credit_card"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order_id | string | 是 | 订单ID |
| uid | string | 是 | 用户ID |
| item_id | int | 是 | 商品ID |
| web_pay_error_code | string | 是 | 支付错误码 |
| web_lang | string | 否 | 网页语言 |
| browser_lang | string | 否 | 浏览器语言 |
| payment_method | string | 否 | 支付方式 |

**常见错误码**:
- `PAYMENT_CANCELLED`: 用户取消支付
- `PAYMENT_FAILED`: 支付失败
- `INSUFFICIENT_FUNDS`: 余额不足
- `NETWORK_ERROR`: 网络错误
- `TIMEOUT`: 支付超时

**成功响应**:
```json
{
  "return_code": 1,
  "msg": "支付失败记录已保存"
}
```

**失败响应**:
```json
{
  "return_code": 0,
  "err_code": 500,
  "msg": "记录失败: 错误信息"
}
```

---

## 📋 订单接口

### 订单历史

获取用户的订单历史记录。

**接口地址**: `POST /api/v1/orders/history`

**请求参数**:
```json
{
  "uid": "12345"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| uid | string | 是 | 用户ID |

**成功响应**:
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
  ]
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| status_code | int | 状态码：1=成功，0=失败 |
| data | array | 订单列表 |

**订单字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| order_id | string | 订单ID |
| item_name | string | 商品名称 |
| order_time | string | 订单时间 |
| order_status | string | 订单状态：completed/failed/pending/cancelled |
| price | float | 订单金额 |
| currency | string | 货币类型 |

**示例代码**:
```bash
curl -X POST "http://localhost:8000/api/v1/orders/history" \
  -H "Content-Type: application/json" \
  -d '{"uid": "12345"}'
```

---

## 🏥 系统接口

### 健康检查

检查API服务运行状态。

**接口地址**: `GET /health`

**请求参数**: 无

**成功响应**:
```json
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | 服务状态 |
| message | string | 状态描述 |

**示例代码**:
```bash
curl -X GET "http://localhost:8000/health"
```

---

## 🧪 测试接口

> **注意**: 以下接口仅在开发环境（DEBUG=True）中可用

### 简单测试

**接口地址**: `GET /test/simple`

**响应**:
```json
{
  "message": "Payment API Test Router is working",
  "status": "ok",
  "timestamp": "2025-09-04"
}
```

### 连通性测试

**接口地址**: `GET /test/ping`

**响应**:
```json
{
  "ping": "pong"
}
```

### Token测试

**接口地址**: `GET /test/token_test`

**响应**:
```json
{
  "return_code": 1,
  "token": "test_token_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "msg": "测试Token获取成功"
}
```

### 登录测试

**接口地址**: `GET /test/login_test`

**响应**:
```json
{
  "status_code": 1,
  "user_id": "test_user_123",
  "user_name": "Test User",
  "level": 10,
  "daily_gift": 1,
  "avatar_url": "https://example.com/avatar.jpg",
  "msg": "测试登录成功"
}
```

### 商城测试

**接口地址**: `GET /test/store_items_test`

### 支付成功测试

**接口地址**: `GET /test/payment_success_test`

### 支付失败测试

**接口地址**: `GET /test/payment_failure_test`

### 订单历史测试

**接口地址**: `GET /test/order_history_test`

### 数据库信息测试

**接口地址**: `GET /test/database_info`

---

## 📊 状态码说明

### HTTP状态码
- `200`: 请求成功
- `400`: 请求参数错误
- `401`: 认证失败或Token无效
- `403`: 权限不足
- `404`: 接口不存在
- `422`: 参数验证失败
- `500`: 服务器内部错误

### 业务状态码
- `return_code: 1`: 业务处理成功
- `return_code: 0`: 业务处理失败
- `status_code: 1`: 操作成功
- `status_code: 0`: 操作失败

### 错误码（err_code）
- `500`: 系统内部错误
- `999`: 通用业务错误
- `401`: 认证错误
- `403`: 权限错误

---

## 🔧 SDK和代码示例

### Python示例
```python
import requests
import json

class PaymentAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
    
    def get_token(self, app_id):
        """获取认证Token"""
        url = f"{self.base_url}/api/v1/token"
        data = {"appId": app_id}
        response = requests.post(url, json=data)
        result = response.json()
        if result.get("return_code") == 1:
            self.token = result.get("token")
            return self.token
        return None
    
    def login(self, login_type, login_id, login_code=None):
        """用户登录"""
        url = f"{self.base_url}/api/v1/login"
        params = {
            "loginType": login_type,
            "loginId": login_id
        }
        if login_code:
            params["loginCode"] = login_code
        
        response = requests.get(url, params=params)
        return response.json()
    
    def get_store_items(self, uid):
        """获取商城商品"""
        url = f"{self.base_url}/api/v1/store/items"
        data = {"uid": uid}
        response = requests.post(url, json=data)
        return response.json()
    
    def payment_success(self, payment_data):
        """支付成功"""
        url = f"{self.base_url}/api/v1/payment/success"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, json=payment_data, headers=headers)
        return response.json()

# 使用示例
client = PaymentAPIClient()
token = client.get_token("com.funtriolimited.slots.casino.free")
if token:
    # 用户登录
    login_result = client.login(1, "facebook123")
    print(f"登录结果: {login_result}")
    
    # 获取商品
    items = client.get_store_items("12345")
    print(f"商品列表: {items}")
    
    # 支付成功
    payment_data = {
        "order_id": "test_order_001",
        "uid": "12345",
        "item_id": 1,
        "price": 19.99,
        "currency": "USD",
        "payment_method": "credit_card",
        "email": "test@example.com"
    }
    result = client.payment_success(payment_data)
    print(f"支付结果: {result}")
```

### JavaScript示例
```javascript
class PaymentAPIClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.token = null;
    }
    
    async getToken(appId) {
        const response = await fetch(`${this.baseUrl}/api/v1/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ appId })
        });
        
        const result = await response.json();
        if (result.return_code === 1) {
            this.token = result.token;
            return this.token;
        }
        return null;
    }
    
    async login(loginType, loginId, loginCode = null) {
        const params = new URLSearchParams({
            loginType,
            loginId
        });
        
        if (loginCode) {
            params.append('loginCode', loginCode);
        }
        
        const response = await fetch(`${this.baseUrl}/api/v1/login?${params}`);
        return await response.json();
    }
    
    async getStoreItems(uid) {
        const response = await fetch(`${this.baseUrl}/api/v1/store/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ uid })
        });
        
        return await response.json();
    }
    
    async paymentSuccess(paymentData) {
        const response = await fetch(`${this.baseUrl}/api/v1/payment/success`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(paymentData)
        });
        
        return await response.json();
    }
}

// 使用示例
const client = new PaymentAPIClient();

async function testAPI() {
    // 获取Token
    const token = await client.getToken('com.funtriolimited.slots.casino.free');
    if (token) {
        console.log('Token获取成功');
        
        // 用户登录
        const loginResult = await client.login(1, 'facebook123');
        console.log('登录结果:', loginResult);
        
        // 获取商品
        const items = await client.getStoreItems('12345');
        console.log('商品列表:', items);
        
        // 支付成功
        const paymentData = {
            order_id: 'test_order_001',
            uid: '12345',
            item_id: 1,
            price: 19.99,
            currency: 'USD',
            payment_method: 'credit_card',
            email: 'test@example.com'
        };
        
        const result = await client.paymentSuccess(paymentData);
        console.log('支付结果:', result);
    }
}

testAPI();
```

---

## 🔗 相关链接

- **项目文档**: [docs/PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **API测试**: [docs/API_TESTING.md](API_TESTING.md)
- **部署指南**: [docs/DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **开发指南**: [docs/DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

> 📝 **注意**: 
> - 所有时间戳使用UTC时间
> - 金额使用美元（USD）为基准
> - Token有效期为3小时，请及时刷新
> - 测试接口仅在开发环境可用
> - 生产环境请使用HTTPS协议