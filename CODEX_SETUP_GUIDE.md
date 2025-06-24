# 🚀 UAI教育平台 - Codex环境设置指南

## 📋 快速开始

### 1️⃣ 环境准备
```bash
# 克隆项目
git clone git@github.com:hy98982002/UAI-coursesApp.git
cd UAI-coursesApp

# 进入后端目录
cd backend
```

### 2️⃣ 配置数据库连接

#### 📝 创建.env文件
将`backend/.env.example`复制为`backend/.env`并填入您的Sealos数据库信息：

```env
# Sealos MySQL 数据库配置
MYSQL_HOST=your-sealos-mysql-host
MYSQL_PORT=your-mysql-port
MYSQL_USER=your-mysql-user
MYSQL_PASSWORD=your-mysql-password
MYSQL_NAME=your-database-name
MYSQL_CHARSET=utf8mb4
MYSQL_CONNECT_TIMEOUT=120
MYSQL_READ_TIMEOUT=120
MYSQL_WRITE_TIMEOUT=120

# Django 配置
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*.codex.io,*.gitpod.io,*.github.dev
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans

# CORS 配置（开发环境）
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
```

### 3️⃣ 一键启动
```bash
# 返回项目根目录
cd ..

# 运行快速启动脚本
chmod +x codex_quick_start.sh
./codex_quick_start.sh
```

## 🔒 安全规范

### ✅ 项目已符合Codex安全标准
- ✅ 所有敏感信息已移至`.env`文件
- ✅ `.env`文件已加入`.gitignore`
- ✅ Django settings使用环境变量
- ✅ 文档中无硬编码凭据
- ✅ 通过安全检查脚本验证

### 🛡️ 安全最佳实践
1. **永远不要在代码中硬编码敏感信息**
2. **使用环境变量管理配置**
3. **确保`.env`文件不被提交到Git**
4. **定期运行安全检查**

## 🔧 手动设置步骤

如果快速启动脚本失败，可以手动执行以下步骤：

### 1. 虚拟环境设置
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
pip install mysql-connector-python python-dotenv
```

### 3. 数据库连接测试
```bash
python -c "
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

conn = mysql.connector.connect(
    host=os.environ['MYSQL_HOST'],
    port=int(os.environ['MYSQL_PORT']),
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_NAME']
)
print('✅ 数据库连接成功!')
conn.close()
"
```

### 4. Django设置
```bash
# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

## 📡 访问地址

启动成功后，您可以访问：

- **主站**: http://localhost:8000
- **管理后台**: http://localhost:8000/admin
- **API文档**: http://localhost:8000/api/

## 🛠️ 故障排除

### 数据库连接问题
1. 检查Sealos数据库是否开启外网访问
2. 验证`.env`文件中的连接信息
3. 确认网络连接正常

### 环境变量问题
1. 检查`.env`文件是否存在
2. 验证环境变量是否正确加载
3. 运行安全检查：`python security_check.py`

### 依赖安装问题
1. 确认Python版本 >= 3.8
2. 更新pip：`pip install --upgrade pip`
3. 手动安装缺失的依赖

## 🔄 开发流程

### 日常开发
```bash
# 激活环境
cd backend && source venv/bin/activate

# 启动服务
python manage.py runserver

# 数据库变更
python manage.py makemigrations
python manage.py migrate
```

### 代码提交前
```bash
# 运行安全检查
python security_check.py

# 确保测试通过
python manage.py test

# 提交代码
git add . && git commit -m "Your message"
```

## 📖 更多文档

- [完整部署指南](CODEX_DEPLOYMENT_GUIDE.md)
- [Sealos连接指南](SEALOS_CODEX_CONNECTION_GUIDE.md)
- [项目架构说明](README.md)

---

🎯 **目标**: 让您在2分钟内启动完整的开发环境
🔒 **承诺**: 符合最高安全标准，保护您的敏感信息 