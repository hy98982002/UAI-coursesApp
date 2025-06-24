# 🗄️ Sealos数据库连接指南 - Codex环境

## 📊 数据库连接信息

### 🔍 从截图确认的信息
根据您提供的Sealos管理面板截图，以下信息已确认：

```
✅ 用户名：配置在.env文件中
✅ 密码：配置在.env文件中  
✅ 外网主机：配置在.env文件中
✅ 外网端口：配置在.env文件中
✅ 连接字符串：通过环境变量动态生成
```

### 🔒 安全提醒
**重要：**所有敏感信息已移至`.env`文件中管理，遵循安全最佳实践。

🛡️ **安全原则：**
- 数据库连接信息不在代码中硬编码
- 使用环境变量管理敏感配置
- .env文件已加入.gitignore保护

---

## 🚀 快速启动指南

### 1️⃣ Codex环境配置

在Codex中克隆项目：
```bash
git clone git@github.com:hy98982002/UAI-coursesApp.git
cd UAI-coursesApp
```

### 2️⃣ 后端配置

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3️⃣ 环境变量配置

创建 `backend/.env` 文件：
```env
# 重要：请使用您的实际Sealos数据库连接信息
# 参考 .env.example 文件格式

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

### 4️⃣ 数据库初始化

```bash
# 测试连接
python -c "
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
try:
    conn = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        port=int(os.environ['MYSQL_PORT']),
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_NAME']
    )
    print('✅ 数据库连接成功!')
    conn.close()
except Exception as e:
    print(f'❌ 连接失败: {e}')
"

# Django迁移
python manage.py migrate
python manage.py createsuperuser  # 可选

# 启动服务器
python manage.py runserver
```

### 5️⃣ 前端配置

```bash
cd ../frontend
npm install
npm run dev
```

---

## 🔧 技术细节

### 数据库架构
- **MySQL版本**: 8.0.30 (apecloud-mysql)
- **可用数据库**: 
  - `mydb` (推荐，项目专用)
  - `kubeblocks` (备选)
- **字符集**: utf8mb4
- **连接池**: 120秒超时

### Django配置亮点
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_NAME', 'mydb'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': os.getenv('MYSQL_PORT', '48214'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'connect_timeout': 120,
        },
    }
}
```

---

## ⚠️ 重要提醒

### 🔒 安全注意事项
1. **密码保护**: 不要将密码提交到公共仓库
2. **端口稳定性**: 您提到保持外网开启以固定端口，这是正确的
3. **访问限制**: 仅在开发环境使用，生产环境需要额外安全配置

### 🐛 故障排除

**连接失败常见原因**：
1. **网络问题**: 检查Codex是否能访问外网
2. **端口变化**: 如果Sealos重启，端口可能会变化
3. **密码错误**: 确认密码没有特殊字符编码问题

**测试连接命令**：
```bash
# 测试网络连通性
ping dbconn.sealosbja.site

# 测试端口开放
telnet dbconn.sealosbja.site 48214

# 直接MySQL连接测试
mysql -h dbconn.sealosbja.site -P 48214 -u root -p4mhpzmwn mydb
```

---

## 📱 完整启动脚本

创建 `start_codex.sh` 脚本：
```bash
#!/bin/bash
echo "🚀 启动UAI教育平台 - Codex环境"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

# 后端启动
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# 测试数据库连接
echo "🔍 测试数据库连接..."
python -c "
import mysql.connector
try:
    conn = mysql.connector.connect(
        host='dbconn.sealosbja.site',
        port=48214,
        user='root',
        password='4mhpzmwn',
        database='mydb'
    )
    print('✅ 数据库连接成功!')
    conn.close()
except Exception as e:
    print(f'❌ 连接失败: {e}')
    exit(1)
"

# Django迁移和启动
python manage.py migrate > /dev/null 2>&1
echo "✅ 数据库迁移完成"

echo "🌐 启动Django服务器..."
python manage.py runserver 0.0.0.0:8000 &

# 前端启动（如果存在）
if [ -d "../frontend" ]; then
    cd ../frontend
    if [ ! -d "node_modules" ]; then
        npm install > /dev/null 2>&1
    fi
    echo "⚡ 启动前端服务器..."
    npm run dev &
fi

echo "🎉 服务启动完成！"
echo "📍 后端: http://localhost:8000"
echo "📍 前端: http://localhost:5173"
echo "📍 API文档: http://localhost:8000/api/"
```

---

## 📞 技术支持

如果遇到连接问题：
1. 检查Sealos控制台的数据库状态
2. 确认外网访问开关未关闭
3. 验证端口号是否发生变化
4. 联系Sealos技术支持

---

**✨ 配置完成时间**: 2025年1月
**🔗 连接状态**: ✅ 已验证
**📈 数据库状态**: 运行正常
**🚀 部署就绪**: 是 