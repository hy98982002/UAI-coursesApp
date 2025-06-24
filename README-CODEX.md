# 🚀 UAI 教育平台 - Codex 环境快速指南

[![Sealos数据库](https://img.shields.io/badge/数据库-Sealos%20MySQL-blue)](https://sealos.io/)
[![Django](https://img.shields.io/badge/后端-Django%205.2-green)](https://djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/前端-Vue%203-brightgreen)](https://vuejs.org/)

> **专为 Codex 云IDE环境优化的部署指南**  
> 支持 Sealos 外网数据库连接，快速启动开发环境

## 🎯 一键启动

### 方法1: 使用快速启动脚本
```bash
# 克隆项目
git clone git@github.com:hy98982002/UAI-coursesApp.git
cd UAI-coursesApp

# 运行快速启动脚本
./start_codex.sh
```

### 方法2: 手动步骤
```bash
# 1. 部署项目
./deploy_codex.sh

# 2. 启动后端（终端1）
cd backend && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000

# 3. 启动前端（终端2）
cd frontend && npm run dev
```

## 📋 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **网络**: 能访问外网（Sealos数据库）
- **内存**: 建议 2GB+

## 🔧 配置数据库

### 自动配置
运行部署脚本会自动创建 `.env` 配置文件：
```bash
./deploy_codex.sh
```

### 手动配置
如果需要手动配置，创建 `backend/.env` 文件：
```bash
cd backend
cp .env.codex.example .env
# 编辑 .env 文件中的数据库配置
```

## 🌐 访问地址

根据 Codex 的端口转发配置：

- **后端API**: `http://localhost:8000/api/`
- **前端界面**: `http://localhost:5173/`
- **Django管理**: `http://localhost:8000/admin/`

## 🔍 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 测试连接
cd backend && python sealos_db_helper.py

# 检查网络
ping dbconn.sealosbia.site
```

#### 2. 端口被占用
```bash
# 查看端口占用
netstat -an | grep :8000
netstat -an | grep :5173

# 杀死进程
pkill -f "runserver"
pkill -f "vite"
```

#### 3. 依赖安装失败
```bash
# 重新安装后端依赖
cd backend && pip install -r requirements.txt

# 重新安装前端依赖
cd frontend && npm install
```

### 网络问题解决

如果在 Codex 中无法连接 Sealos 数据库：

1. **检查代理设置**
```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

2. **测试网络连通性**
```bash
curl -I http://dbconn.sealosbia.site:30758
```

3. **调整超时设置**
在 `backend/.env` 中增加：
```
MYSQL_CONNECT_TIMEOUT=180
MYSQL_READ_TIMEOUT=180
MYSQL_WRITE_TIMEOUT=180
```

## 📊 项目结构

```
UAI-coursesApp/
├── backend/                    # Django 后端
│   ├── .env                   # 数据库配置（需创建）
│   ├── .env.codex.example     # 配置模板
│   ├── sealos_db_helper.py    # 数据库连接测试
│   └── manage.py              # Django 管理工具
├── frontend/                   # Vue.js 前端
│   ├── src/                   # 源代码
│   └── package.json           # Node.js 依赖
├── deploy_codex.sh            # 一键部署脚本
├── start_codex.sh             # 快速启动脚本
└── CODEX_DEPLOYMENT_GUIDE.md  # 详细部署指南
```

## 🚀 开发工作流

### 日常开发
```bash
# 启动开发环境
./start_codex.sh

# 查看日志
tail -f backend/logs/uai.log

# 数据库操作
cd backend && python manage.py shell
cd backend && python manage.py migrate
```

### 代码更新
```bash
# 拉取最新代码
git pull origin master

# 重新安装依赖（如有更新）
cd backend && pip install -r requirements.txt
cd frontend && npm install

# 数据库迁移
cd backend && python manage.py migrate
```

## 🛠️ VS Code 配置

推荐在 Codex 中安装以下扩展：

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "Vue.volar",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

### 调试配置

创建 `.vscode/launch.json`：
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/manage.py",
      "args": ["runserver", "0.0.0.0:8000"],
      "django": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

## 📈 性能优化

### 数据库连接优化
在 `backend/.env` 中设置：
```
MYSQL_CONNECT_TIMEOUT=120
MYSQL_READ_TIMEOUT=120
MYSQL_WRITE_TIMEOUT=120
```

### 前端构建优化
```bash
# 开发环境（快速热更新）
npm run dev

# 生产构建
npm run build
```

## 🔐 安全注意事项

1. **环境变量保护**
   - `.env` 文件已在 `.gitignore` 中
   - 不要将数据库密码提交到代码仓库

2. **访问控制**
   - Codex 环境通常是私有的
   - 生产环境需要配置防火墙规则

## 📚 相关文档

- [完整部署指南](CODEX_DEPLOYMENT_GUIDE.md)
- [Sealos部署说明](CODEX_SEALOS_DEPLOYMENT.md)
- [项目技术栈](UAI_MVP_Tech_Stack.md)
- [API文档](新版UAI测试接口文档.md)

## 🆘 获取帮助

### 快速诊断
```bash
# 运行诊断脚本
cd backend && python sealos_db_helper.py --verbose

# 检查项目状态
./start_codex.sh  # 选择选项 5（测试数据库连接）
```

### 常用命令
```bash
# 重置环境
rm -rf backend/venv frontend/node_modules
./deploy_codex.sh

# 查看进程
ps aux | grep python
ps aux | grep node

# 停止服务
pkill -f "runserver"
pkill -f "vite"
```

---

**🎉 享受在 Codex 中的开发体验！**

> 如有问题，请查看详细的 [CODEX_DEPLOYMENT_GUIDE.md](CODEX_DEPLOYMENT_GUIDE.md) 文档 