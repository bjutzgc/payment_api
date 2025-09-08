# Payment API 部署指南

## 📋 部署概述

本文档提供Payment API项目的完整部署指南，包括开发环境、测试环境和生产环境的部署方案，以及性能优化、安全配置和监控设置。

## 🏗️ 部署架构

### 系统架构图
```mermaid
graph TB
    A[用户请求] --> B[负载均衡器]
    B --> C[FastAPI应用服务器]
    C --> D[MySQL数据库]
    C --> E[Redis缓存]
    C --> F[日志服务]
    
    subgraph "应用服务器集群"
    C1[FastAPI实例1]
    C2[FastAPI实例2]
    C3[FastAPI实例3]
    end
    
    subgraph "数据层"
    D1[主数据库]
    D2[从数据库]
    E1[Redis主节点]
    E2[Redis从节点]
    end
```

### 部署组件
- **Web服务器**: Nginx (反向代理 + 静态文件)
- **应用服务器**: Uvicorn (ASGI服务器)
- **数据库**: MySQL 8.0+ (主从复制)
- **缓存**: Redis 6.x+ (哨兵模式)
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack (可选)

## 🛠️ 环境准备

### 系统要求
- **操作系统**: Linux (Ubuntu 20.04+ / CentOS 8+)
- **Python**: 3.8+
- **内存**: 最小2GB，推荐4GB+
- **磁盘**: 最小10GB可用空间
- **网络**: 稳定的网络连接

### 基础软件安装

#### Ubuntu/Debian
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Python和依赖
sudo apt install python3 python3-pip python3-venv -y

# 安装MySQL
sudo apt install mysql-server mysql-client -y

# 安装Redis
sudo apt install redis-server -y

# 安装Nginx
sudo apt install nginx -y

# 安装进程管理工具
sudo apt install supervisor -y
```

#### CentOS/RHEL
```bash
# 更新系统
sudo yum update -y

# 安装Python和依赖
sudo yum install python3 python3-pip -y

# 安装MySQL
sudo yum install mysql-server mysql -y

# 安装Redis
sudo yum install redis -y

# 安装Nginx
sudo yum install nginx -y

# 安装进程管理工具
sudo yum install supervisor -y
```

## 🚀 应用部署

### 1. 项目部署

#### 创建部署用户
```bash
# 创建专用用户
sudo useradd -m -s /bin/bash payment
sudo usermod -aG sudo payment

# 切换到部署用户
sudo su - payment
```

#### 部署项目代码
```bash
# 创建项目目录
mkdir -p /home/payment/apps
cd /home/payment/apps

# 克隆或上传项目代码
git clone <your-repo-url> payment_api
cd payment_api

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建必要目录
mkdir -p logs
mkdir -p static
chmod 755 logs
```

### 2. 环境配置

#### 生产环境配置
```bash
# 创建生产环境配置
export ENVIRONMENT=online

# 或者创建环境变量文件
cat > .env << EOF
ENVIRONMENT=online
DEBUG=False
PROJECT_NAME=Payment API
PROJECT_VERSION=1.0.0

# 数据库配置
DATABASE_URLS={"default":"mysql+aiomysql://payment_user:secure_password@localhost:3306/vegas_production","ro":"mysql+aiomysql://payment_user:secure_password@slave-db:3306/vegas_production","rw":"mysql+aiomysql://payment_user:secure_password@localhost:3306/vegas_production"}

# Redis配置
REDIS_CONF={"vegas":{"host":"localhost","port":6379,"db_id":0,"password":"redis_password"},"vegas_fb":{"host":"localhost","port":6379,"db_id":1,"password":"redis_password"}}

# JWT配置
JWT_SECRET_KEY=your_super_secure_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=3

# CORS配置
ALLOW_ORIGINS=["https://yourdomain.com","https://api.yourdomain.com"]
ALLOW_CREDENTIALS=true
ALLOW_METHODS=["GET","POST","PUT","DELETE"]
ALLOW_HEADERS=["*"]
EOF
```

### 3. 数据库设置

#### MySQL配置
```bash
# 登录MySQL
sudo mysql -u root -p

# 创建数据库和用户
CREATE DATABASE vegas_production CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'payment_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON vegas_production.* TO 'payment_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 初始化数据库表（如果需要）
cd /home/payment/apps/payment_api
source venv/bin/activate
python -c "
from src.database import init_database
init_database()
"
```

#### Redis配置
```bash
# 编辑Redis配置
sudo nano /etc/redis/redis.conf

# 修改以下配置
bind 127.0.0.1
port 6379
requirepass redis_password
maxmemory 256mb
maxmemory-policy allkeys-lru

# 重启Redis
sudo systemctl restart redis
sudo systemctl enable redis
```

## ⚙️ 服务配置

### 1. Uvicorn服务配置

#### 创建启动脚本
```bash
# 创建启动脚本
cat > /home/payment/apps/payment_api/start_production.sh << 'EOF'
#!/bin/bash
cd /home/payment/apps/payment_api
source venv/bin/activate
export ENVIRONMENT=online
exec uvicorn src.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --access-log \
    --log-level info \
    --no-use-colors
EOF

chmod +x /home/payment/apps/payment_api/start_production.sh
```

#### Supervisor配置
```bash
# 创建Supervisor配置
sudo cat > /etc/supervisor/conf.d/payment_api.conf << 'EOF'
[program:payment_api]
command=/home/payment/apps/payment_api/start_production.sh
directory=/home/payment/apps/payment_api
user=payment
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/payment/apps/payment_api/logs/payment_api.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
environment=ENVIRONMENT="online"

[group:payment_services]
programs=payment_api
EOF

# 重新加载Supervisor配置
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start payment_api
```

### 2. Nginx配置

#### 反向代理配置
```bash
# 创建Nginx配置
sudo cat > /etc/nginx/sites-available/payment_api << 'EOF'
upstream payment_backend {
    server 127.0.0.1:8000;
    # 如果有多个实例
    # server 127.0.0.1:8001;
    # server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    # HTTP重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    # SSL证书配置
    ssl_certificate /etc/ssl/certs/yourdomain.com.pem;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # 限制请求体大小
    client_max_body_size 10M;
    
    # 访问日志
    access_log /var/log/nginx/payment_api_access.log;
    error_log /var/log/nginx/payment_api_error.log;
    
    # API代理
    location /api/ {
        proxy_pass http://payment_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # 缓冲设置
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://payment_backend;
        access_log off;
    }
    
    # API文档（仅开发环境）
    location /docs {
        proxy_pass http://payment_backend;
        # 生产环境可以注释掉或添加访问控制
    }
    
    # 静态文件
    location /static/ {
        alias /home/payment/apps/payment_api/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # 限流配置
    location / {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://payment_backend;
    }
}

# 限流配置
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
}
EOF

# 启用站点
sudo ln -s /etc/nginx/sites-available/payment_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔐 安全配置

### 1. 防火墙设置
```bash
# 使用UFW配置防火墙
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允许必要端口
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 限制数据库访问（仅本地）
sudo ufw deny 3306
sudo ufw deny 6379
```

### 2. SSL证书配置
```bash
# 使用Let's Encrypt免费证书
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d api.yourdomain.com

# 自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. 系统安全加固
```bash
# 禁用root SSH登录
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl reload sshd

# 配置fail2ban
sudo apt install fail2ban -y
sudo cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/payment_api_error.log
maxretry = 10
findtime = 600
bantime = 7200
EOF

sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## 📊 监控配置

### 1. 系统监控

#### Prometheus配置
```bash
# 安装Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
sudo mv prometheus-2.40.0.linux-amd64 /opt/prometheus
sudo useradd --no-create-home --shell /bin/false prometheus
sudo chown -R prometheus:prometheus /opt/prometheus

# 创建配置文件
sudo cat > /opt/prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'payment-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
EOF

# 创建Systemd服务
sudo cat > /etc/systemd/system/prometheus.service << 'EOF'
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/opt/prometheus/prometheus \
    --config.file=/opt/prometheus/prometheus.yml \
    --storage.tsdb.path=/opt/prometheus/data \
    --web.console.templates=/opt/prometheus/consoles \
    --web.console.libraries=/opt/prometheus/console_libraries \
    --web.listen-address=0.0.0.0:9090

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable prometheus
sudo systemctl start prometheus
```

### 2. 应用监控

#### 添加应用指标
```python
# 在main.py中添加Prometheus指标
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# 定义指标
REQUEST_COUNT = Counter('payment_api_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('payment_api_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method, 
        endpoint=request.url.path
    ).inc()
    REQUEST_DURATION.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

### 3. 日志监控
```bash
# 配置日志轮转
sudo cat > /etc/logrotate.d/payment_api << 'EOF'
/home/payment/apps/payment_api/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 payment payment
    postrotate
        supervisorctl restart payment_api
    endscript
}
EOF
```

## 🔄 部署流程

### 1. 自动化部署脚本
```bash
#!/bin/bash
# deploy.sh - 自动化部署脚本

set -e

PROJECT_DIR="/home/payment/apps/payment_api"
BACKUP_DIR="/home/payment/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "🚀 开始部署 Payment API..."

# 1. 创建备份
echo "📦 创建备份..."
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/payment_api_$TIMESTAMP.tar.gz -C $(dirname $PROJECT_DIR) $(basename $PROJECT_DIR)

# 2. 更新代码
echo "📥 更新代码..."
cd $PROJECT_DIR
git pull origin main

# 3. 更新依赖
echo "📦 更新依赖..."
source venv/bin/activate
pip install -r requirements.txt

# 4. 数据库迁移（如果需要）
echo "🗄️ 数据库迁移..."
# python manage.py migrate  # 如果使用alembic

# 5. 重启服务
echo "🔄 重启服务..."
sudo supervisorctl restart payment_api

# 6. 健康检查
echo "🏥 健康检查..."
sleep 5
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 部署成功！"
else
    echo "❌ 部署失败，正在回滚..."
    tar -xzf $BACKUP_DIR/payment_api_$TIMESTAMP.tar.gz -C $(dirname $PROJECT_DIR)
    sudo supervisorctl restart payment_api
    exit 1
fi

echo "🎉 部署完成！"
```

### 2. CI/CD集成

#### GitHub Actions示例
```yaml
name: Deploy Payment API

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.4
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/payment/apps/payment_api
          ./deploy.sh
```

## 🔧 性能优化

### 1. 数据库优化
```sql
-- MySQL优化配置
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB
SET GLOBAL innodb_log_file_size = 268435456;     -- 256MB
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_flush_log_at_trx_commit = 2;

-- 创建索引
CREATE INDEX idx_user_facebook_id ON users(facebook_id);
CREATE INDEX idx_order_user_id ON orders(user_id);
CREATE INDEX idx_order_created_at ON orders(created_at);
```

### 2. Redis优化
```bash
# Redis配置优化
echo 'vm.overcommit_memory = 1' >> /etc/sysctl.conf
echo 'net.core.somaxconn = 65535' >> /etc/sysctl.conf
sysctl -p
```

### 3. 应用优化
```python
# 连接池配置
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600
}

# Redis连接池
REDIS_CONFIG = {
    "max_connections": 100,
    "retry_on_timeout": True
}
```

## 📋 运维检查清单

### 部署前检查
- [ ] 系统资源充足（CPU、内存、磁盘）
- [ ] 网络连接正常
- [ ] 数据库连接配置正确
- [ ] Redis服务正常
- [ ] SSL证书有效
- [ ] 防火墙规则配置
- [ ] 监控服务运行

### 部署后验证
- [ ] 健康检查接口响应正常
- [ ] API功能测试通过
- [ ] 数据库连接正常
- [ ] Redis缓存工作正常
- [ ] 日志输出正确
- [ ] 监控指标正常
- [ ] 性能测试通过

### 日常维护
- [ ] 检查服务状态
- [ ] 监控系统资源使用
- [ ] 查看错误日志
- [ ] 备份数据库
- [ ] 更新SSL证书
- [ ] 清理旧日志文件
- [ ] 性能优化调整

## 🆘 故障排除

### 常见问题

#### 1. 服务启动失败
```bash
# 检查日志
sudo supervisorctl tail payment_api stderr

# 检查端口占用
netstat -tlnp | grep :8000

# 检查配置文件
python -c "from src.web_config import settings; print(settings)"
```

#### 2. 数据库连接问题
```bash
# 测试数据库连接
mysql -u payment_user -p -h localhost vegas_production

# 检查数据库服务
sudo systemctl status mysql
```

#### 3. Redis连接问题
```bash
# 测试Redis连接
redis-cli -a redis_password ping

# 检查Redis服务
sudo systemctl status redis
```

#### 4. 性能问题
```bash
# 检查系统负载
top
htop
iostat -x 1

# 检查应用性能
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/health"
```

## 📞 支持联系

如果遇到部署问题，请检查：
1. 系统日志：`/var/log/syslog`
2. 应用日志：`/home/payment/apps/payment_api/logs/`
3. Nginx日志：`/var/log/nginx/`
4. 监控面板：Prometheus/Grafana

---

> 📝 **注意**: 
> - 请根据实际环境调整配置参数
> - 定期备份重要数据
> - 保持系统和依赖更新
> - 监控安全补丁发布
> 
> 🔗 **相关文档**:
> - 参考 `docs/API_TESTING.md` 了解API测试
> - 查看 `docs/PROJECT_STRUCTURE.md` 了解项目结构