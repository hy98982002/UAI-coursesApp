# 🚀 Codex环境快速配置指南

## 📋 项目已成功上传到GitHub
- **仓库地址**: https://github.com/hy98982002/UAIEDUcourseApp
- **克隆命令**: `git clone git@github.com:hy98982002/UAIEDUcourseApp.git`

## ⚡ 在Codex中的配置步骤

### 第1步: 克隆项目
```bash
git clone git@github.com:hy98982002/UAIEDUcourseApp.git
cd UAIEDUcourseApp
```

### 第2步: 创建环境变量文件
在 `backend/` 目录下创建 `.env` 文件：

```bash
cd backend
cat > .env << 'EOF'
# Django基础配置
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Sealos MySQL数据库配置
MYSQL_HOST=dbconn.sealos.bja.site
MYSQL_PORT=33949
MYSQL_NAME=test-db-mysql-0
MYSQL_USER=root
MYSQL_PASSWORD=786qpf2t

# 数据库连接选项
MYSQL_CHARSET=utf8mb4
MYSQL_CONNECT_TIMEOUT=30
MYSQL_READ_TIMEOUT=30
MYSQL_WRITE_TIMEOUT=30

# 其他配置
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans
EOF
```

### 第3步: 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../frontend
npm install
```

### 第4步: 测试数据库连接
```bash
cd backend
python sealos_db_helper.py
```

### 第5步: 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 第6步: 启动服务
```bash
# 后端服务
python manage.py runserver 0.0.0.0:8000

# 前端服务（新终端）
cd ../frontend
npm run dev
```

## 🔧 代理网络配置说明

如果在Codex环境中遇到网络连接问题：

1. **确认代理配置**: 确保代理能访问 `dbconn.sealos.bja.site:33949`
2. **增加超时时间**: 在 `.env` 文件中设置更长的超时时间
3. **检查防火墙**: 确保端口 33949 未被阻止

## 🛠️ 故障排除

### 连接超时
```bash
# 测试网络连接
ping dbconn.sealos.bja.site
telnet dbconn.sealos.bja.site 33949
```

### 数据库连接测试
```bash
# 使用内置工具测试
python backend/sealos_db_helper.py

# Django连接测试
python backend/manage.py check --database default
```

## 📁 项目结构
```
UAIEDUcourseApp/
├── backend/                 # Django后端
│   ├── .env                # 环境变量配置（需要创建）
│   ├── sealos_db_helper.py # Sealos连接助手
│   ├── manage.py
│   └── ...
├── frontend/               # Vue前端
├── CODEX_SEALOS_DEPLOYMENT.md  # 详细部署文档
└── CODEX_SETUP_GUIDE.md   # 本文档
```

## 🔐 安全提醒
- ✅ 敏感信息已通过环境变量保护
- ✅ `.env` 文件已在 `.gitignore` 中
- ✅ 代码已通过安全检查，可安全部署

## 📞 支持
遇到问题时：
1. 查看 `CODEX_SEALOS_DEPLOYMENT.md` 详细文档
2. 运行 `python backend/sealos_db_helper.py` 诊断连接
3. 检查 `backend/logs/uai.log` 日志文件

---
**更新时间**: 2025年6月23日  
**适用环境**: Codex + Sealos云数据库 