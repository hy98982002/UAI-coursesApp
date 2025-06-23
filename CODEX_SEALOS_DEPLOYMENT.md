# 🚀 UAI教育平台 - Codex + Sealos 部署指南

## 📋 概述

本指南详细说明如何在Codex环境中通过代理网络连接到Sealos数据库，实现UAI教育平台的云端部署。

## 🔧 前置准备

### 1. Sealos数据库信息
- **外网地址**: `your-sealos-host:33949`
- **内网地址**: `your-internal-host:3306`
- **数据库名**: `your-database-name`
- **用户名**: `root`
- **密码**: `your-database-password`

### 2. 技术栈
- **后端**: Django 5.2 + DRF + MySQL
- **前端**: Vue 3 + Vite + Bootstrap 5
- **数据库**: Sealos托管MySQL 8.0

## ⚡ 快速部署步骤

### 步骤1: 创建环境变量文件

在 `backend/` 目录下创建 `.env` 文件：

```bash
# ==========================================
# UAI教育平台 Sealos数据库配置
# ==========================================

# Sealos MySQL数据库配置（外网访问，适合Codex代理）
MYSQL_HOST=your-sealos-host
MYSQL_PORT=33949
MYSQL_NAME=your-database-name
MYSQL_USER=root
MYSQL_PASSWORD=your-database-password

# 数据库连接选项
MYSQL_CHARSET=utf8mb4
MYSQL_CONNECT_TIMEOUT=30
MYSQL_READ_TIMEOUT=30
MYSQL_WRITE_TIMEOUT=30

# Django配置
SECRET_KEY=your-secret-key-here-please-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans
```

### 步骤2: 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 步骤3: 测试数据库连接

```bash
# 使用自定义连接助手
python sealos_db_helper.py

# 或者使用Django命令
python manage.py check --database default
```

### 步骤4: 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 步骤5: 启动服务

```bash
# 后端服务
python manage.py runserver 0.0.0.0:8000

# 前端服务（新终端）
cd ../frontend
npm install
npm run dev
```

## 🔧 Codex环境特殊配置

### 代理网络设置

由于Codex可能需要通过代理访问外网，请确保：

1. **网络连接**: 确认代理网络能够访问 `dbconn.sealos.bja.site`
2. **防火墙**: 确保端口 `33949` 未被阻止
3. **超时设置**: 已配置较长的连接超时时间（30秒）

### 环境变量检查

使用内置工具验证配置：

```python
# 快速验证数据库连接
from sealos_db_helper import quick_test
quick_test()

# 获取Django配置
from sealos_db_helper import SealosDBHelper
helper = SealosDBHelper()
db_config = helper.get_django_db_config()
print(db_config)
```

## 🛠️ 故障排除

### 常见问题

#### 1. 连接超时
```
Error: 2005 (HY000): Unknown MySQL server host 'dbconn.sealos.bja.site'
```

**解决方案**:
- 检查网络连接
- 确认代理配置正确
- 尝试增加连接超时时间

#### 2. 认证失败
```
Error: 1045 (28000): Access denied for user 'root'@'xxx'
```

**解决方案**:
- 确认用户名密码正确
- 检查数据库权限设置

#### 3. 数据库不存在
```
Error: 1049 (42000): Unknown database 'test-db-mysql-0'
```

**解决方案**:
```python
from sealos_db_helper import SealosDBHelper
helper = SealosDBHelper()
helper.create_database_if_not_exists()
```

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Django设置
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## 📁 项目结构

```
UAI_project/
├── backend/
│   ├── .env                    # 环境变量配置
│   ├── .env.example           # 环境变量模板
│   ├── sealos_db_helper.py    # Sealos连接助手
│   ├── manage.py
│   ├── uai_backend/
│   │   ├── settings.py        # 已配置Sealos支持
│   │   └── ...
│   └── apps/
├── frontend/
└── CODEX_SEALOS_DEPLOYMENT.md  # 本文档
```

## 🔐 安全注意事项

1. **永远不要提交 `.env` 文件到Git**
2. **在生产环境中更改默认密码**
3. **使用强密钥生成SECRET_KEY**
4. **生产环境设置 DEBUG=False**

## 📞 支持

如果在Codex环境中遇到问题：

1. 运行 `python sealos_db_helper.py` 进行诊断
2. 检查网络代理设置
3. 确认Sealos数据库服务状态
4. 查看Django日志文件：`backend/logs/uai.log`

---

**最后更新**: 2025年6月23日
**适用版本**: UAI MVP v1.0 