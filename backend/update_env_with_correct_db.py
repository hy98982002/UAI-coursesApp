#!/usr/bin/env python3
"""
更新.env文件使用正确的数据库名称
"""

# 使用mydb数据库（更适合我们的项目）
env_content = """# Sealos MySQL 数据库配置（2025年1月最新）
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
"""

# 写入.env文件
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ .env配置文件已更新")
print("📊 使用数据库: mydb")
print("🌐 连接字符串: mysql://root:4mhpzmwn@dbconn.sealosbja.site:48214/mydb")

# 测试连接到mydb
import mysql.connector
from mysql.connector import Error

try:
    config = {
        'host': 'dbconn.sealosbja.site',
        'port': 48214,
        'user': 'root',
        'password': '4mhpzmwn',
        'database': 'mydb',
        'charset': 'utf8mb4',
        'connect_timeout': 120
    }
    
    connection = mysql.connector.connect(**config)
    
    if connection.is_connected():
        print("✅ 成功连接到mydb数据库!")
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   📋 现有表: {[table[0] for table in tables]}")
        else:
            print("   📋 数据库为空，完美适合Django项目")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 数据库配置完成！可以开始Django开发")
        
except Error as e:
    print(f"❌ 连接测试失败: {e}")
    
    # 如果mydb失败，提供kubeblocks作为备选
    print("\n💡 备选方案：使用kubeblocks数据库")
    print("如果需要，可以手动将MYSQL_NAME改为kubeblocks") 