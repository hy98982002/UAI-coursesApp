#!/bin/bash
# 🚀 UAI教育平台 - Codex环境快速启动脚本

echo "🚀 启动UAI教育平台 - Codex环境"
echo "="*50

# 检查当前目录
if [ ! -f "README.md" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 后端配置
echo "📦 配置后端环境..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -q -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "📝 创建.env配置文件..."
    cat > .env << 'EOF'
# Sealos MySQL 数据库配置（2025年1月最新）
MYSQL_HOST=dbconn.sealosbja.site
MYSQL_PORT=48214
MYSQL_USER=root
MYSQL_PASSWORD=4mhpzmwn
MYSQL_NAME=mydb
MYSQL_CHARSET=utf8mb4
MYSQL_CONNECT_TIMEOUT=120
MYSQL_READ_TIMEOUT=120
MYSQL_WRITE_TIMEOUT=120

# Django 配置
SECRET_KEY=django-insecure-uai-education-platform-2025
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*.codex.io,*.gitpod.io,*.github.dev
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans

# CORS 配置（开发环境）
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
EOF
    echo "✅ .env文件已创建"
fi

# 测试数据库连接
echo "🔍 测试Sealos数据库连接..."
python -c "
import mysql.connector
try:
    conn = mysql.connector.connect(
        host='dbconn.sealosbja.site',
        port=48214,
        user='root',
        password='4mhpzmwn',
        database='mydb',
        connect_timeout=10
    )
    print('✅ 数据库连接成功!')
    cursor = conn.cursor()
    cursor.execute('SELECT VERSION()')
    version = cursor.fetchone()
    print(f'📊 MySQL版本: {version[0]}')
    conn.close()
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    print('💡 请检查网络连接和Sealos数据库状态')
    exit 1
"

# Django迁移
echo "🔄 执行数据库迁移..."
python manage.py migrate --verbosity=0

# 检查是否已有管理员用户
echo "👤 检查管理员用户..."
python -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('💡 建议创建超级用户: python manage.py createsuperuser')
else:
    print('✅ 管理员用户已存在')
"

echo "🌐 启动Django开发服务器..."
echo "📍 后端API: http://localhost:8000/"
echo "📍 Django管理: http://localhost:8000/admin/"
echo "📍 API文档: http://localhost:8000/api/"
echo ""
echo "🚀 服务器启动中..."
echo "按 Ctrl+C 停止服务器"

python manage.py runserver 0.0.0.0:8000 