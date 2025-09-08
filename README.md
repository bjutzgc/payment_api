# Payment API - FastAPI版本

这是从Django REST Framework转换而来的FastAPI版本的支付API系统。

## 技术栈

- **FastAPI**: 现代、快速的Web框架
- **SQLModel**: 基于Pydantic和SQLAlchemy的ORM
- **Redis**: 缓存和会话存储
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI服务器

## 项目结构

```
src/
├── __init__.py
├── main.py              # FastAPI主应用
├── config.py            # 配置管理
├── database.py          # 数据库连接配置
├── models.py            # SQLModel数据模型
├── schemas.py           # Pydantic输入/输出模式
├── constants.py         # 常量定义
├── redis_service.py     # Redis服务
├── game_service.py      # 游戏业务逻辑
└── routers/
    ├── __init__.py
    ├── api_routes.py    # 主要API路由
    └── test_routes.py   # 测试路由
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

复制环境变量示例文件并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库和Redis连接。

### 3. 启动应用

```bash
python run.py
```

或者直接使用uvicorn：

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 访问API文档

启动后访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 主要端点

- `GET/POST /` - 首页
- `GET/POST /mytest` - 测试接口
- `GET/POST /user_msg` - 用户消息
- `GET/POST /activity` - 活动信息
- `GET/POST /user_purchase` - 用户购买

### 测试端点

- `GET /test/test_user_msg` - 测试用户消息
- `GET /test/test_activity` - 测试活动
- `GET /test/test_user_purchase` - 测试购买

### 健康检查

- `GET /health` - 健康检查

## 数据库配置

### SQLite (默认)

```env
DATABASE_URL=sqlite:///./payment_api.db
```

### PostgreSQL

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

### MySQL

```env
DATABASE_URL=mysql+aiomysql://user:password@localhost/dbname
```

## Redis配置

在 `.env` 文件中配置Redis连接，或者在 `src/config.py` 中直接修改：

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

## 从Django迁移的主要变化

1. **ORM**: Django ORM → SQLModel
2. **序列化**: Django REST Framework Serializers → Pydantic Schemas
3. **路由**: Django URL patterns → FastAPI routers
4. **中间件**: Django middleware → FastAPI middleware
5. **配置**: Django settings → Pydantic settings
6. **异步支持**: 原生异步支持

## 开发注意事项

1. 所有API端点支持自动的请求/响应验证
2. 自动生成的API文档
3. 内置的依赖注入系统
4. 更好的类型提示和IDE支持
5. 更高的性能

## 测试

```bash
pytest
```

## 📚 详细文档

我们为项目提供了完整的文档集合，位于 `docs/` 目录：

- **[📋 项目结构与环境说明](docs/PROJECT_STRUCTURE.md)** - 项目架构、技术栈和环境配置
- **[🧪 API测试文档](docs/API_TESTING.md)** - 完整的API测试指南和示例
- **[🚀 部署指南](docs/DEPLOYMENT_GUIDE.md)** - 生产环境部署完整方案
- **[💻 开发指南](docs/DEVELOPMENT_GUIDE.md)** - 开发规范和最佳实践
- **[📖 API接口参考](docs/API_REFERENCE.md)** - 详细的接口文档和SDK示例
- **[📚 文档中心](docs/README.md)** - 文档导航和使用指南

## 🚀 快速部署

### 开发环境
```bash
# 快速启动
python run.py

# 或使用uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境
```bash
# 生产部署
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

> 📖 **详细部署说明**: 请参考 [部署指南](docs/DEPLOYMENT_GUIDE.md) 获取完整的部署方案。

## 🧪 API测试

### 快速测试
```bash
# 健康检查
curl -X GET "http://localhost:8000/health"

# 获取Token
curl -X POST "http://localhost:8000/api/v1/token" \
  -H "Content-Type: application/json" \
  -d '{"appId": "com.funtriolimited.slots.casino.free"}'

# 测试登录
curl -X GET "http://localhost:8000/api/v1/login?loginType=1&loginId=test123"
```

> 🧪 **完整测试指南**: 请参考 [API测试文档](docs/API_TESTING.md) 获取详细的测试方法。

## 💡 主要特性

### 🔐 安全认证
- JWT Token认证（3小时有效期）
- 多种登录方式支持（Facebook、Google、Apple等）
- 安全的API访问控制

### 🛒 商城系统
- 动态商品配置
- 首充识别和奖励
- 用户等级权限控制

### 💰 支付处理
- 支付成功/失败处理
- 动态奖励计算
- 订单历史管理

### 🔧 技术优势
- 异步数据库操作
- Redis缓存支持
- 多数据库配置
- 自动API文档生成

## 🤝 贡献指南

欢迎贡献代码和改进建议！

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

> 💻 **开发规范**: 请参考 [开发指南](docs/DEVELOPMENT_GUIDE.md) 了解详细的开发规范。

## 📞 支持与反馈

- **API文档**: http://localhost:8000/docs (Swagger UI)
- **问题报告**: [GitHub Issues](https://github.com/your-org/payment_api/issues)
- **功能建议**: [GitHub Discussions](https://github.com/your-org/payment_api/discussions)
- **技术支持**: 查看 [文档中心](docs/README.md) 获取帮助

## 📄 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.