#!/usr/bin/env python3
"""
创建Sealos数据库连接的.env配置文件
"""

# 最新的Sealos数据库配置
env_content = """# Sealos MySQL 数据库配置（2025年1月最新）
MYSQL_HOST=dbconn.sealosbja.site
MYSQL_PORT=48214
MYSQL_USER=root
MYSQL_PASSWORD=4mhpzmwn
MYSQL_NAME=test-db-mysql-0
MYSQL_CHARSET=utf8mb4
MYSQL_CONNECT_TIMEOUT=120
MYSQL_READ_TIMEOUT=120
MYSQL_WRITE_TIMEOUT=120

# Django 配置
SECRET_KEY=django-insecure-change-this-in-production-2025
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,*.codex.io,*.gitpod.io,*.github.dev
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans

# CORS 配置（开发环境）
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOW_CREDENTIALS=True
"""

# 写入.env文件
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ .env配置文件已创建")
print("📊 数据库连接信息:")
print("   主机: dbconn.sealosbja.site")
print("   端口: 48214")
print("   用户: root")
print("   数据库: test-db-mysql-0") 