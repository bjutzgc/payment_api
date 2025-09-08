# 超简单API测试

覆盖所有核心功能的超简单测试，包括：
- ✅ 获取Token
- ✅ 用户登录
- ✅ 获取商城信息
- ✅ 每日奖励
- ✅ 支付成功
- ✅ 支付失败
- ✅ 获取历史订单

## 🚀 快速开始

### 1. 启动服务
```bash
# 在项目根目录启动服务
python run.py
```

### 2. 运行测试

#### 方法1: Python脚本测试（推荐）
```bash
python test/simple_test.py
```

#### 方法2: curl脚本测试
```bash
# 给脚本执行权限
chmod +x test/curl_test.sh

# 运行测试（需要安装jq）
./test/curl_test.sh
```

#### 方法3: pytest测试
```bash
# 安装pytest
pip install pytest requests

# 运行测试
pytest test/test_api.py -v
```

## 📋 测试内容

| 功能 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 健康检查 | `/health` | GET | 服务状态检查 |
| 获取Token | `/api/v1/token` | POST | 获取3小时有效期的JWT token |
| 用户登录 | `/api/v1/login` | GET | 多种登录方式支持 |
| 每日奖励 | `/api/v1/daily_gift` | POST | 领取每日礼物 |
| 商城信息 | `/api/v1/store/items` | POST | 获取用户可购买商品 |
| 支付成功 | `/api/v1/payment/success` | POST | 支付成功回调（需token） |
| 支付失败 | `/api/v1/payment/failure` | POST | 支付失败记录（需token） |
| 历史订单 | `/api/v1/orders/history` | POST | 获取用户订单历史 |

## 🔧 测试参数

- **测试用户ID**: `test123`
- **应用ID**: `com.funtriolimited.slots.casino.free`
- **基础URL**: `http://localhost:8000`

## 📝 注意事项

1. **Token认证**: 支付相关接口需要先获取token
2. **用户存在**: 登录测试可能因用户不存在而失败，这是正常的
3. **服务运行**: 确保API服务在localhost:8000运行
4. **依赖安装**: curl测试需要安装`jq`工具

## 🛠️ 依赖

- **Python脚本**: `requests`
- **curl脚本**: `curl`, `jq`
- **pytest**: `pytest`, `requests`

## 🎯 预期结果

正常情况下，所有接口都应该返回HTTP 200状态码。具体业务逻辑结果可能因数据状态而异：

- ✅ 健康检查：正常返回
- ✅ Token获取：成功获取token
- ⚠️ 登录：可能因用户不存在而失败
- ✅ 每日奖励：正常响应
- ✅ 商城信息：返回商品列表
- ✅ 支付成功：正常处理
- ✅ 支付失败：正常记录
- ✅ 历史订单：返回订单列表

## 🔍 故障排除

1. **连接失败**: 确认API服务正在运行
2. **Token获取失败**: 检查appId是否正确
3. **支付接口401**: 确认token获取成功且未过期