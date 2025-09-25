# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service.py  # 支付处理核心逻辑
│   │   └── redis_service.py    # Redis连接管理
│   ├── constants.py            # 常量定义
│   ├── item_configs.py         # 商品配置与奖励规则
│   ├── main.py                 # FastAPI应用主入口
│   ├── models.py               # SQLModel 数据模型
│   ├── web_config_local.py     # 本地开发环境配置
│   └── web_config_online.py    # 生产环境配置
├── test/                       # 测试脚本
│   ├── basic_test.py           # 基础功能测试
│   ├── curl_test.sh            # curl 命令测试
│   └── test_api.py             # API接口测试
├── requirements.txt            # Python依赖
├── run.py                      # 启动脚本
└── README.md                   # 项目文档
```

## 🛠 技术栈

### 核心框架
- **[FastAPI](https://fastapi.tiangolo.com/)** `^0.104.1` - 现代化异步Web框架
- **[SQLModel](https://sqlmodel.tiangolo.com/)** `^0.0.14` - 类型安全的ORM
- **[Pydantic](https://pydantic.dev/)** `^2.5.0` - 数据验证和序列化
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI服务器

### 数据存储
- **MySQL** - 主数据库 (通过 aiomysql/PyMySQL)
- **Redis** `^5.0.1` - 缓存和会话存储
- **SQLite** - 开发环境备选

### 安全认证
- **JWT Token** - JSON Web Token 认证
- **python-jose** - JWT 加密解密
- **passlib** - 密码哈希处理

### 开发工具
- **pytest** - 单元测试框架
- **httpx** - HTTP客户端测试
- **alembic** - 数据库迁移

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite
- Redis 5.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd payment_api
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境

根据运行环境修改配置文件：

- **开发环境**: 编辑 `src/web_config_local.py`
- **生产环境**: 编辑 `src/web_config_online.py`

### 4. 启动服务

```bash
# 开发环境 (自动重载)
python run.py

# 或直接使用 uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境 (多进程)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 验证服务

```bash
# 健康检查
curl http://localhost:8000/health

# 查看API文档
open http://localhost:8000/docs
```

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📋 订单管理
- `GET /api/v1/orders/history` - 订单历史查询

### 🎁 奖励系统
- `POST /api/v1/daily_gift` - 每日奖励领取

### 🔧 系统接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付平台回调 `/api/v1/payment/success`
4. 系统更新用户金币，发放奖励到收件箱

### 权限与奖励规则
- **普通用户** (金币 < 10000 或 等级 < 99.99): 可购买前6个商品
- **高级用户** (金币 ≥ 10000 且 等级 ≥ 99.99): 可购买全部8个商品
- **首充用户**: 购买任意商品额外获得 10%-25% 奖励

## 🗄 数据库配置

### MySQL (推荐)
```python
# src/web_config_local.py 或 src/web_config_online.py
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/payment_db"
```

### SQLite (开发环境)
```python
DATABASE_URL = "sqlite:///./payment_api.db"
```

### Redis 配置
```python
REDIS_CONF = {
    "forever_new_user": {
        "host": "localhost",
        "port": 6379,
        "db_id": 0
    },
    "forever_new_fb": {
        "host": "localhost",
        "port": 6379,
        "db_id": 1
    }
}
```

## 🧪 测试



运行测试套件：

```bash
# 运行所有测试
pytest test/

# 运行特定测试文件
pytest test/test_api.py -v

# 运行并查看覆盖率
pytest --cov=src test/
```

### 快速API测试

```bash
# 使用内置测试脚本
python test/quick_test.py

# 使用curl测试脚本
bash test/curl_test.sh
```

### 手动测试示例

```bash
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚀 部署指南

### 开发环境部署

1. **设置环境变量**
   ```bash
   export ENV=local  # 使用本地开发配置
   ```

2. **启动开发服务器**
   ```bash
   python run.py
   ```

### 生产环境部署

1. **设置环境变量**
   ```bash
   export ENV=online  # 使用生产环境配置
   ```

2. **多进程启动**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **使用Gunicorn + Uvicorn**
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Docker部署

项目包含完整的Docker配置：

```bash
# 构建镜像
docker build -t payment-api .

# 运行容器
docker run -d -p 8000:8000 --name payment-api-container payment-api

# 使用docker-compose
docker-compose up -d
```

### 反向代理配置 (Nginx)

``nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 安全配置

### JWT配置
- Token有效期：3小时
- 支持的登录类型：Facebook(1)、Google(2)、Apple(3)、邮箱(4)、短信(5)
- 安全的密钥管理和Token刷新机制

### 生产环境安全检查清单
- [ ] 修改默认JWT密钥
- [ ] 启用HTTPS
- [ ] 配置CORS白名单
- [ ] 设置速率限制
- [ ] 启用请求日志
- [ ] 定期备份数据库
- [ ] 监控异常访问

## 📊 监控与日志

### 健康检查
```bash
# 服务状态检查
curl http://localhost:8000/health

# 响应示例
{
  "status": "healthy",
  "message": "Payment API is running"
}
```

### 日志配置
- **开发环境**: INFO级别，控制台输出
- **生产环境**: WARNING级别，文件输出
- 支持结构化日志和请求追踪

## 🔧 故障排查

### 常见问题

**1. 数据库连接失败**
```bash
# 检查数据库连接
mysql -h localhost -u username -p

# 检查配置文件
cat src/web_config_local.py | grep DATABASE_URL
```

**2. Redis连接问题**
```bash
# 测试Redis连接
redis-cli ping

# 检查Redis配置
cat src/web_config_local.py | grep REDIS_CONF
```

**3. 端口占用**
```bash
# 查看端口占用
lsof -i :8000

# 杀死占用进程
kill -9 <PID>
```

**4. 启动失败**
- 检查Python版本 (需要3.8+)
- 确认所有依赖已安装
- 查看错误日志获取详细信息

## 🤝 开发指南

### 代码风格
- 遵循PEP 8代码规范
- 使用类型注解
- 编写完整的文档字符串

### 提交代码
1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### API开发规范
- 使用Pydantic模型进行数据验证
- 遵循RESTful设计原则
- 提供详细的响应示例
- 添加适当的错误处理

## 📞 技术支持

### 文档资源
- **API文档**: http://localhost:8000/docs (开发环境)
- **交互式文档**: http://localhost:8000/redoc
- **技术博客**: [FastAPI官方文档](https://fastapi.tiangolo.com/)

### 获取帮助
- **问题报告**: 在GitHub Issues中提交
- **功能建议**: 通过GitHub Discussions讨论
- **技术交流**: 查看项目Wiki获取更多信息

### 版本历史
- **v1.0.0**: 初始版本，基础支付功能
- **v1.1.0**: 添加多平台登录支持
- **v1.2.0**: 增强商品管理和奖励系统

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**构建时间**: 2024年
**技术栈**: FastAPI + SQLModel + Redis + MySQL
**维护状态**: 🟢 积极维护

> 💡 **提示**: 如果您在使用过程中遇到任何问题，请先查看[故障排查](#-故障排查)部分，或者在GitHub Issues中搜索相关问题。
```

```
# Payment API

支付API服务，提供用户登录、商品购买、支付处理等功能。

## 🚀 快速开始

### 环境要求
- Python 3.8+
- MySQL 5.7+ 或 SQLite (开发环境)
- Redis 5.0+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
python run.py
```

服务将运行在 `http://localhost:8000`

## 📚 API 接口概览

### 🔐 认证相关
- `POST /api/v1/token` - 获取访问令牌
- `GET /api/v1/login` - 用户登录
- `POST /api/v1/refresh` - 刷新用户信息

### 🛒 商城系统
- `GET /api/v1/store/items` - 获取商品列表
- `POST /api/v1/payment/success` - 支付成功回调
- `POST /api/v1/payment/failure` - 支付失败记录

### 📖 其他接口
- `GET /health` - 健康检查
- `GET /docs` - API文档 (Swagger UI)
- `GET /redoc` - API文档 (ReDoc)

## 💡 核心业务流程

### 用户登录流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌
2. 使用令牌调用 `/api/v1/login` 完成登录
3. 服务端返回用户信息（ID、等级、金币等）

### 刷新用户信息流程
1. 客户端调用 `/api/v1/token` 获取JWT令牌（如果需要）
2. 使用令牌调用 `/api/v1/refresh` 接口，传入用户ID
3. 服务端验证令牌并返回最新的用户信息

### 商品购买流程
1. 客户端请求 `/api/v1/store/items` 获取商品列表
2. 用户选择商品，发起支付
3. 支付成功后调用 `/api/v1/payment/success` 回调
4. 服务端处理支付结果并发放奖励

## 🧪 测试命令

```
# 1. 健康检查
curl -X GET "http://localhost:8000/health"

# 2. 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 3. 用户登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. 刷新用户信息
curl -X POST "http://localhost:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "uid": "12345"
  }'

# 5. 获取商品列表
curl -X GET "http://localhost:8000/api/v1/store/items" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📁 项目结构

```
.
├── src/                        # 源代码目录
│   ├── routers/                # 路由模块
│   │   ├── payment_routes.py   # 支付相关API路由
│   │   └── test_routes.py      # 测试用路由
│   ├── schemas/                # Pydantic 数据模式
│   │   └── payment_schemas.py  # 支付相关数据模型
│   ├── service/                # 业务逻辑服务层
│   │   ├── db_service.py       # 数据库会话管理
│   │   ├── game_service.py     # 游戏业务逻辑
│   │   ├── login_service.py    # 登录服务
│   │   ├── payment_service