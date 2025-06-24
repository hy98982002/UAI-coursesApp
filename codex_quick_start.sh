#!/bin/bash
# UAI项目 Codex 快速启动脚本
# 符合安全规范，不包含硬编码敏感信息

echo "🚀 UAI教育平台 - Codex快速启动"
echo "==============================="

# 进入backend目录
cd backend || {
    echo "❌ backend目录不存在"
    exit 1
}

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "❌ .env配置文件不存在！"
    echo "📝 请手动创建 backend/.env 文件，参考 .env.example"
    echo "💡 包含数据库连接信息：MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD"
    exit 1
fi

# 激活虚拟环境
if [ -d "venv" ]; then
    echo "🐍 激活Python虚拟环境..."
    source venv/bin/activate || source venv/Scripts/activate
else
    echo "⚠️  虚拟环境不存在，使用系统Python"
fi

# 安装依赖
echo "📦 检查Python依赖..."
pip install -q mysql-connector-python python-dotenv 2>/dev/null || echo "⚠️  依赖安装可能需要手动处理"

# 加载环境变量
echo "🔧 加载环境变量..."
export $(cat .env | grep -v '^#' | xargs) 2>/dev/null

# 测试数据库连接
echo "🔍 测试Sealos数据库连接..."
python -c "
import mysql.connector
import os
try:
    conn = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        port=int(os.environ['MYSQL_PORT']),
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_NAME'],
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
echo "🔧 执行Django数据库迁移..."
python manage.py makemigrations 2>/dev/null || echo "⚠️  makemigrations可能有问题"
python manage.py migrate || {
    echo "❌ 数据库迁移失败"
    exit 1
}

# 创建超级用户（可选）
echo "👤 创建Django超级用户（可选，按Ctrl+C跳过）..."
python manage.py createsuperuser --noinput --username admin --email admin@uai.edu 2>/dev/null || echo "ℹ️  超级用户已存在或需要交互创建"

# 启动开发服务器
echo "🌐 启动Django开发服务器..."
echo "📡 访问地址: http://localhost:8000"
echo "🔧 管理后台: http://localhost:8000/admin"
echo "📋 API文档: http://localhost:8000/api/"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "==============================="

python manage.py runserver 0.0.0.0:8000 