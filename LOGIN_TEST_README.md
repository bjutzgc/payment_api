# Payment API 登录接口 CURL 测试命令集合

## 基础信息
- 服务地址：http://localhost:8000
- API基础路径：http://localhost:8000/api/v1

## 各种登录方式测试命令

### 1. Facebook登录
```bash
curl -X GET "http://localhost:8000/api/v1/login?login_type=1&login_id=facebook_test_id_12345" \
  -H "accept: application/json"
```

### 2. Google登录
```bash
curl -X GET "http://localhost:8000/api/v1/login?login_type=2&login_id=google_test_id_67890" \
  -H "accept: application/json"
```

### 3. UserToken登录
```bash
# 注意：需要替换为真实有效的JWT token
curl -X GET "http://localhost:8000/api/v1/login?login_type=3&login_id=dummy&user_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwidGVzdCI6dHJ1ZSwiaWF0IjoxNjk5OTk5OTk5LCJleHAiOjE3MDAwMDM1OTl9.test_signature" \
  -H "accept: application/json"
```

### 4. 邮箱登录
```bash
curl -X GET "http://localhost:8000/api/v1/login?login_type=4&login_id=test@example.com&login_code=123456" \
  -H "accept: application/json"
```

### 5. SMS登录
```bash
curl -X GET "http://localhost:8000/api/v1/login?login_type=5&login_id=%2B1234567890&login_code=654321" \
  -H "accept: application/json"
```

### 6. Apple登录
```bash
curl -X GET "http://localhost:8000/api/v1/login?login_type=6&login_id=apple_test_id_99999" \
  -H "accept: application/json"
```

## 参数验证测试

### 测试无效登录类型
```bash
curl -X GET "http://localhost:8000/api/v1/login?login_type=99&login_id=test" \
  -H "accept: application/json"
```

### 测试缺少必需参数
```bash
# 缺少login_id
curl -X GET "http://localhost:8000/api/v1/login?login_type=1" \
  -H "accept: application/json"

# UserToken登录缺少user_token
curl -X GET "http://localhost:8000/api/v1/login?login_type=3&login_id=test" \
  -H "accept: application/json"

# 邮箱登录缺少验证码
curl -X GET "http://localhost:8000/api/v1/login?login_type=4&login_id=test@example.com" \
  -H "accept: application/json"
```

## 测试结果说明

### 正常响应结构
```json
{
  "uid": "12345",
  "user_name": "User_12345",
  "level": 1,
  "avatar_url": "https://example.com/avatar.jpg",
  "show": 0,
  "return_code": null,
  "status_code": 1,
  "err_code": null,
  "msg": "登录成功",
  "daily_gift": 1
}
```

### 错误响应结构
```json
{
  "uid": null,
  "user_name": null,
  "level": null,
  "avatar_url": null,
  "show": null,
  "return_code": null,
  "status_code": 0,
  "err_code": null,
  "msg": "用户不存在",
  "daily_gift": null
}
```

## 登录类型说明
- `login_type=1`: Facebook登录，需要 `login_id` (Facebook ID)
- `login_type=2`: Google登录，需要 `login_id` (Google ID)
- `login_type=3`: UserToken登录，需要 `login_id` (任意值) + `user_token` (JWT Token)
- `login_type=4`: 邮箱登录，需要 `login_id` (邮箱地址) + `login_code` (验证码)
- `login_type=5`: SMS登录，需要 `login_id` (手机号) + `login_code` (验证码)
- `login_type=6`: Apple登录，需要 `login_id` (Apple ID)

## 注意事项
1. 测试使用的是示例数据，实际用户可能不存在，会返回"用户不存在"
2. UserToken登录需要使用真实有效的JWT token
3. 邮箱和SMS登录需要有效的验证码
4. 确保数据库中有对应的测试用户数据
5. URL中的特殊字符需要进行URL编码（如+号编码为%2B）

## API文档访问
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health