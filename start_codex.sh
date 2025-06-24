#!/bin/bash

echo "🚀 UAI 教育平台 - Codex 快速启动脚本"
echo "================================"
echo ""

# 检查是否在项目根目录
if [ ! -f "deploy_codex.sh" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 检查后端配置
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到 backend/.env 文件"
    echo "正在从模板创建..."
    if [ -f "backend/.env.codex.example" ]; then
        cp backend/.env.codex.example backend/.env
        echo "✅ 已创建 .env 文件，请根据需要修改配置"
    else
        echo "❌ 模板文件不存在，请手动创建 .env 文件"
        exit 1
    fi
fi

# 选择启动模式
echo "请选择启动模式："
echo "1) 完整部署（首次运行，包含安装依赖）"
echo "2) 快速启动（仅启动服务）"
echo "3) 仅启动后端"
echo "4) 仅启动前端"
echo "5) 测试数据库连接"
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "🔧 执行完整部署..."
        ./deploy_codex.sh
        ;;
    2)
        echo "🚀 快速启动服务..."
        echo "启动后端服务（在后台运行）..."
        cd backend
        source venv/bin/activate
        nohup python manage.py runserver 0.0.0.0:8000 > ../logs/backend.log 2>&1 &
        echo "后端服务已启动 (PID: $!)"
        cd ..
        
        echo "启动前端服务..."
        cd frontend
        npm run dev &
        echo "前端服务已启动"
        cd ..
        
        echo ""
        echo "✅ 服务启动完成！"
        echo "后端: http://localhost:8000"
        echo "前端: http://localhost:5173"
        echo "查看后端日志: tail -f logs/backend.log"
        ;;
    3)
        echo "🔗 启动后端服务..."
        cd backend
        source venv/bin/activate
        python manage.py runserver 0.0.0.0:8000
        ;;
    4)
        echo "🎨 启动前端服务..."
        cd frontend
        npm run dev
        ;;
    5)
        echo "🔍 测试数据库连接..."
        cd backend
        source venv/bin/activate
        python sealos_db_helper.py
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac 