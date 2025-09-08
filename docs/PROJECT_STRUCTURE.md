# Payment API 项目结构与环境说明

## 📋 项目概述

本项目是从 Django REST Framework 迁移至 FastAPI 的支付API系统，提供高效、可靠的支付接口，支持多种数据库和异步处理。项目采用现代化的架构设计，具有更高的性能和更好的开发体验。

## 🗂️ 项目目录结构

```
payment_api/
├── src/                         # 核心源代码目录
│   ├── routers/                 # 路由模块
│   │   ├── payment_routes.py    # 支付相关路由（Token、登录、支付、商城等）
│   │   └── test_routes.py       # 测试路由（开发环境专用）
│   ├── schemas/                 # 数据模式定义
│   │   ├── __init__.py
│   │   └── payment_schemas.py   # 支付相关的请求/响应模式
│   ├── service/                 # 业务服务层
│   │   ├── __init__.py          # 服务模块统一导入接口
│   │   ├── db_service.py        # 数据库服务（多数据库支持）
│   │   ├── game_service.py      # 游戏业务逻辑服务
│   │   ├── login_service.py     # 登录服务（多登录类型支持）
│   │   ├── payment_service.py   # 支付处理服务
│   │   └── redis_service.py     # Redis缓存服务
│   ├── constants.py             # 项目常量定义
│   ├── item_configs.py          # 商品配置管理
│   ├── main.py                  # FastAPI主应用入口
│   ├── models.py                # SQLModel数据模型
│   ├── web_config_local.py      # 本地开发环境配置
│   └── web_config_online.py     # 生产环境配置
├── docs/                        # 项目文档目录（本目录）
├── tests/                       # 测试文件
│   ├── test_api_complete.py     # 完整API测试
│   ├── test_dynamic_store.py    # 动态商城测试
│   ├── test_item_configs.py     # 商品配置测试
│   ├── test_payment_api.py      # 支付API测试
│   └── test_purchase_success.py # 购买成功流程测试
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── run.py                       # 本地运行脚本
└── simple_test.py               # 简单测试脚本
```

## 🏗️ 架构设计

### 分层架构
- **Router Layer**: 处理HTTP请求和响应
- **Service Layer**: 核心业务逻辑处理
- **Data Layer**: 数据库操作和缓存管理
- **Config Layer**: 配置管理和环境适配

### 设计模式
- **MVC模式**: 路由、服务、模型分离
- **工厂模式**: 数据库连接和Redis服务初始化
- **单例模式**: 配置管理和缓存服务
- **依赖注入**: FastAPI原生支持

## 💻 技术栈

### 核心框架
- **FastAPI 0.104.1**: 现代、快速的Web框架
- **SQLModel 0.0.14**: 基于Pydantic和SQLAlchemy的ORM
- **Pydantic 2.5.0**: 数据验证和序列化
- **Uvicorn 0.24.0**: ASGI服务器

### 数据库支持
- **SQLite**: 默认开发数据库
- **MySQL**: 生产环境（aiomysql + PyMySQL）
- **PostgreSQL**: 可选支持（asyncpg）

### 缓存和安全
- **Redis 5.0.1**: 缓存和会话存储
- **JWT**: Token认证（python-jose）
- **bcrypt**: 密码加密（passlib）

### 开发工具
- **pytest 7.4.3**: 单元测试框架
- **httpx 0.25.2**: 异步HTTP客户端
- **alembic 1.13.1**: 数据库迁移工具

## 🌍 环境配置

### 开发环境配置（Local）
```python
# src/web_config_local.py
DEBUG = True
DATABASE_URLS = {
    "default": "mysql+aiomysql://root:123456@localhost:3306/vegas",
    "ro": "mysql+aiomysql://root:123456@localhost:3306/vegas",
    "rw": "mysql+aiomysql://root:123456@localhost:3306/vegas",
}
REDIS_CONF = {
    "vegas": {"host": "localhost", "port": 6379, "db_id": 0},
    "vegas_fb": {"host": "localhost", "port": 6379, "db_id": 1}
}
```

### 生产环境配置（Online）
```python
# src/web_config_online.py
DEBUG = False
DATABASE_URLS = {
    "default": "mysql+aiomysql://payment_user:prod_password@prod-db-master:3306/vegas_production",
    "ro": "mysql+aiomysql://payment_user:prod_password@prod-db-slave:3306/vegas_production",
    "rw": "mysql+aiomysql://payment_user:prod_password@prod-db-master:3306/vegas_production",
}
# 支持读写分离和集群配置
```

### 环境切换
通过 `ENVIRONMENT` 环境变量控制：
- `local`: 本地开发环境
- `online`: 生产环境

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装Python依赖
pip install -r requirements.txt

# 准备Redis服务
# 确保Redis 6.x+ 运行在localhost:6379

# 准备数据库
# MySQL: 创建vegas数据库
# 或使用默认SQLite数据库
```

### 2. 配置设置
```bash
# 复制环境配置示例（如果存在）
cp .env.example .env

# 编辑配置文件（可选，使用代码中默认配置）
# 编辑 src/web_config_local.py 进行本地配置调整
```

### 3. 启动应用
```bash
# 方式1: 使用项目运行脚本
python run.py

# 方式2: 直接使用uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 方式3: 使用main.py
cd src && python main.py
```

### 4. 访问服务
- **API文档**: http://localhost:8000/docs (Swagger UI)
- **API文档**: http://localhost:8000/redoc (ReDoc)
- **健康检查**: http://localhost:8000/health
- **测试接口**: http://localhost:8000/test/simple (开发环境)

## 🔧 配置管理

### 多环境配置
项目采用混合配置管理模式：
1. **代码默认配置**: 提供基础配置值
2. **环境配置文件**: 特定环境配置覆盖
3. **环境变量**: 最高优先级配置

### 数据库配置
支持多数据库配置：
```python
DATABASE_URLS = {
    "default": "主数据库连接",
    "ro": "只读数据库连接", 
    "rw": "读写数据库连接"
}
```

### Redis配置
支持多Redis实例：
```python
REDIS_CONF = {
    "vegas": {"host": "localhost", "port": 6379, "db_id": 0},
    "vegas_fb": {"host": "localhost", "port": 6379, "db_id": 1}
}
```

## 🔐 安全特性

### JWT Token认证
- **Token有效期**: 3小时
- **加密算法**: HS256
- **Bearer认证**: 标准HTTP认证方式

### 参数验证
- **自动验证**: Pydantic模型自动验证请求参数
- **类型安全**: 强类型检查和转换
- **错误处理**: 详细的验证错误信息

### 安全配置
- **CORS**: 跨域资源共享配置
- **密钥管理**: 环境变量管理敏感信息
- **SQL注入防护**: SQLModel ORM防护

## 📊 性能特性

### 异步支持
- **异步数据库**: 支持异步MySQL、PostgreSQL
- **异步Redis**: 异步缓存操作
- **异步处理**: 全链路异步处理

### 连接池管理
- **数据库连接池**: 自动管理数据库连接
- **Redis连接池**: 高效的缓存连接管理
- **资源复用**: 优化资源使用效率

### 高并发支持
- **ASGI服务器**: Uvicorn高性能服务器
- **事件循环**: 基于异步事件循环
- **无阻塞IO**: 非阻塞IO操作

## 🧪 测试环境

### 测试数据库
- **开发测试**: 使用本地MySQL/SQLite
- **集成测试**: 模拟生产环境配置
- **单元测试**: 内存数据库测试

### 测试工具
- **pytest**: 单元测试和集成测试
- **httpx**: API接口测试
- **测试路由**: 开发环境测试接口

## 📈 监控和日志

### 日志配置
- **开发环境**: DEBUG级别，详细日志
- **生产环境**: WARNING级别，关键日志
- **结构化日志**: 时间戳、模块、级别、消息

### 健康检查
- **健康检查接口**: `/health`
- **服务状态监控**: 实时服务状态检测
- **依赖检查**: 数据库、Redis连接检查

## 🔄 部署说明

### 开发部署
```bash
python run.py
# 自动启用热重载、API文档、测试路由
```

### 生产部署
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
# 多进程、生产优化、安全配置
```

### Docker部署
```dockerfile
# 可创建Dockerfile进行容器化部署
# 支持标准容器化部署流程
```

## 🛠️ 开发工具

### IDE支持
- **类型提示**: 完整的类型注解支持
- **自动补全**: IDE智能提示
- **错误检查**: 静态类型检查

### 调试工具
- **FastAPI调试**: 自动重载和错误页面
- **日志调试**: 详细的日志输出
- **API文档**: 交互式API测试界面

### 代码质量
- **类型检查**: Pydantic模型验证
- **代码规范**: Python标准编码规范
- **测试覆盖**: 全面的测试用例

---

> 📝 **注意**: 本文档随项目更新，请确保使用最新版本的配置和说明。
> 🔗 **相关文档**: 参考 `docs/API_TESTING.md` 了解API测试详情。