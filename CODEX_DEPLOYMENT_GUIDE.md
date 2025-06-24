# 🚀 Codex 环境完整部署指南

> **专为在 Codex 环境中运行 UAI 教育平台项目设计**  
> 包含 Sealos 数据库连接、环境配置和故障排除

## 📋 项目信息
- **GitHub 仓库**: https://github.com/hy98982002/UAI-coursesApp.git
- **数据库**: Sealos 外网 MySQL
- **框架**: Django + Vue.js

## 🎯 快速开始

### 步骤 1: 在 Codex 中克隆项目
```bash
# 打开 Codex 终端
git clone git@github.com:hy98982002/UAI-coursesApp.git
cd UAI-coursesApp
```

### 步骤 2: 配置后端环境
```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者在 Windows 中: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 3: 配置数据库连接
```bash
# 创建环境变量文件
cat > .env << 'EOF'
# Django 配置
SECRET_KEY=django-insecure-your-secret-key-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*.codex.io

# Sealos MySQL 数据库配置
MYSQL_NAME=test-db-mysql-0
MYSQL_USER=root
MYSQL_PASSWORD=4mhgzmwn
MYSQL_HOST=dbconn.sealosbia.site
MYSQL_PORT=30758
MYSQL_CHARSET=utf8mb4

# 连接优化配置
MYSQL_CONNECT_TIMEOUT=60
MYSQL_READ_TIMEOUT=60
MYSQL_WRITE_TIMEOUT=60

# 国际化
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans
EOF
```

### 步骤 4: 测试数据库连接
```bash
# 使用内置的数据库连接测试工具
python sealos_db_helper.py

# 如果连接成功，继续数据库迁移
python manage.py check --database default
python manage.py migrate
```

### 步骤 5: 启动后端服务
```bash
# 启动 Django 开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 步骤 6: 配置前端（新终端）
```bash
cd frontend

# 安装 Node.js 依赖
npm install

# 启动前端开发服务器
npm run dev
```

## 🌐 Codex 网络配置

### 网络访问说明
Codex 环境通常具有出站网络访问能力，可以连接外部数据库：

```bash
# 测试网络连接
ping dbconn.sealosbia.site
nslookup dbconn.sealosbia.site

# 测试端口连通性
telnet dbconn.sealosbia.site 30758
# 或者使用 nc
nc -zv dbconn.sealosbia.site 30758
```

### 代理配置（如果需要）
如果 Codex 环境使用代理：

```bash
# 设置代理环境变量
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
export NO_PROXY=localhost,127.0.0.1

# 测试代理连接
curl -I http://dbconn.sealosbia.site:30758
```

## 🐛 故障排除

### 问题 1: 数据库连接超时
**现象**: `OperationalError: (2005, "Unknown server host")`

**解决方案**:
```bash
# 1. 增加超时时间
echo "MYSQL_CONNECT_TIMEOUT=120" >> backend/.env
echo "MYSQL_READ_TIMEOUT=120" >> backend/.env
echo "MYSQL_WRITE_TIMEOUT=120" >> backend/.env

# 2. 检查 DNS 解析
nslookup dbconn.sealosbia.site

# 3. 尝试直接 IP 连接（如果知道 IP）
# 将 MYSQL_HOST 改为实际 IP 地址
```

### 问题 2: 权限错误
**现象**: `Access denied for user 'root'`

**解决方案**:
```bash
# 检查密码是否正确
cat backend/.env | grep MYSQL_PASSWORD

# 尝试直接连接测试
mysql -h dbconn.sealosbia.site -P 30758 -u root -p
```

### 问题 3: 端口被阻止
**现象**: `Connection refused`

**解决方案**:
```bash
# 检查端口是否开放
nc -zv dbconn.sealosbia.site 30758

# 尝试其他工具
python3 -c "
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('dbconn.sealosbia.site', 30758))
print('Port is open' if result == 0 else 'Port is closed')
sock.close()
"
```

### 问题 4: SSL/TLS 连接问题
**解决方案**:
```bash
# 在 .env 文件中添加 SSL 配置
echo "MYSQL_OPTIONS_ssl_disabled=True" >> backend/.env

# 或者启用 SSL（如果 Sealos 要求）
echo "MYSQL_OPTIONS_ssl_verify_cert=False" >> backend/.env
echo "MYSQL_OPTIONS_ssl_verify_identity=False" >> backend/.env
```

## 🔧 高级配置

### 环境变量完整列表
```bash
# 完整的 .env 配置示例
cat > backend/.env << 'EOF'
# ===================
# Django 基础配置
# ===================
SECRET_KEY=django-insecure-your-very-long-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*.codex.io,*.gitpod.io

# ===================
# 数据库配置
# ===================
MYSQL_NAME=test-db-mysql-0
MYSQL_USER=root
MYSQL_PASSWORD=4mhgzmwn
MYSQL_HOST=dbconn.sealosbia.site
MYSQL_PORT=30758
MYSQL_CHARSET=utf8mb4

# ===================
# 连接优化
# ===================
MYSQL_CONNECT_TIMEOUT=120
MYSQL_READ_TIMEOUT=120
MYSQL_WRITE_TIMEOUT=120

# ===================
# SSL 配置（根据需要启用）
# ===================
# MYSQL_OPTIONS_ssl_disabled=True
# MYSQL_OPTIONS_ssl_verify_cert=False

# ===================
# 国际化
# ===================
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans

# ===================
# 开发配置
# ===================
CORS_ALLOW_ALL_ORIGINS=True
EOF
```

### 生产环境配置
```bash
# 为生产环境生成安全的 SECRET_KEY
python -c "
from django.core.management.utils import get_random_secret_key
print('SECRET_KEY=' + get_random_secret_key())
" >> backend/.env
```

## 🚀 部署脚本

创建一键部署脚本：

```bash
cat > deploy_codex.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 开始部署 UAI 教育平台到 Codex..."

# 检查环境
echo "📋 检查环境依赖..."
python3 --version
node --version
npm --version

# 后端配置
echo "⚙️ 配置后端..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 测试数据库连接
echo "🔗 测试数据库连接..."
python sealos_db_helper.py

# 数据库迁移
echo "📊 执行数据库迁移..."
python manage.py migrate

# 前端配置
echo "🎨 配置前端..."
cd ../frontend
npm install

echo "✅ 部署完成！"
echo ""
echo "启动命令："
echo "后端: cd backend && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000"
echo "前端: cd frontend && npm run dev"
EOF

chmod +x deploy_codex.sh
```

## 📊 监控和日志

### 查看应用日志
```bash
# Django 日志
tail -f backend/logs/uai.log

# 数据库连接日志
python backend/sealos_db_helper.py --verbose
```

### 性能监控
```bash
# 检查数据库连接性能
python -c "
import time
import MySQLdb
start = time.time()
try:
    conn = MySQLdb.connect(
        host=os.environ['MYSQL_HOST'],
        port=30758,
        user='root',
        password=os.environ['MYSQL_PASSWORD'],
        database='test-db-mysql-0'
    )
    print(f'连接成功，耗时: {time.time() - start:.2f}s')
    conn.close()
except Exception as e:
    print(f'连接失败: {e}')
"
```

## 📱 Codex 特定配置

### VS Code 扩展推荐
在 Codex 中安装以下扩展以提升开发体验：

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-vscode.vscode-json",
    "Vue.volar",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

### 端口转发配置
```bash
# 在 Codex 中配置端口转发
# 后端: 8000
# 前端: 5173 (Vite 默认端口)
```

## 🆘 支持和帮助

### 常用命令速查表
```bash
# 重启数据库连接
python backend/manage.py shell -c "from django.db import connection; connection.close()"

# 清理缓存
python backend/manage.py collectstatic --clear

# 创建超级用户
python backend/manage.py createsuperuser

# 检查项目配置
python backend/manage.py check

# 查看数据库状态
python backend/manage.py dbshell
```

### 获取帮助
1. **项目文档**: 查看项目根目录下的其他 `.md` 文件
2. **数据库助手**: 运行 `python backend/sealos_db_helper.py --help`
3. **Django 文档**: https://docs.djangoproject.com/
4. **Vue 文档**: https://vuejs.org/guide/

---

**🎉 祝您在 Codex 环境中开发愉快！**

> 如遇问题，请检查网络连接并确保 Sealos 数据库服务正常运行。 