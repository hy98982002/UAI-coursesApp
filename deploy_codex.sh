#!/bin/bash
set -e

echo "🚀 开始部署 UAI 教育平台到 Codex..."
echo "===================================="

# 检查环境
echo "📋 检查环境依赖..."
python3 --version
echo "Node版本:"
node --version
echo "NPM版本:"
npm --version
echo ""

# 后端配置
echo "⚙️ 配置后端环境..."
cd backend

# 检查是否已有虚拟环境
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，请手动创建并配置数据库连接信息"
    echo "参考CODEX_DEPLOYMENT_GUIDE.md中的配置示例"
    exit 1
fi

# 测试数据库连接
echo "🔗 测试数据库连接..."
if python sealos_db_helper.py; then
    echo "✅ 数据库连接成功"
else
    echo "❌ 数据库连接失败，请检查网络和配置"
    echo "提示: 可能需要在Codex中配置网络访问权限"
fi

# 数据库迁移
echo "📊 执行数据库迁移..."
python manage.py check --database default
python manage.py migrate

# 创建超级用户（可选）
read -p "是否创建Django超级用户? (y/N): " create_superuser
if [[ $create_superuser =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# 返回项目根目录
cd ..

# 前端配置
echo "🎨 配置前端环境..."
cd frontend

# 安装Node.js依赖
echo "安装Node.js依赖..."
npm install

# 返回项目根目录
cd ..

echo ""
echo "✅ 部署完成！"
echo "===================================="
echo ""
echo "🚀 启动命令："
echo "后端服务:"
echo "  cd backend && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000"
echo ""
echo "前端服务:"
echo "  cd frontend && npm run dev"
echo ""
echo "📝 其他有用命令："
echo "  查看数据库状态: cd backend && python sealos_db_helper.py"
echo "  Django管理: cd backend && python manage.py --help"
echo "  创建超级用户: cd backend && python manage.py createsuperuser"
echo ""
echo "🌐 访问地址（根据Codex端口转发配置）："
echo "  后端API: http://localhost:8000/"
echo "  前端界面: http://localhost:5173/"
echo "  Django管理后台: http://localhost:8000/admin/"
echo ""
echo "📖 详细文档: 查看 CODEX_DEPLOYMENT_GUIDE.md" 