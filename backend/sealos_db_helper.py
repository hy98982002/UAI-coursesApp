#!/usr/bin/env python3
"""
Sealos数据库连接帮助工具
专为Codex环境设计，支持代理网络访问
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SealosDBHelper:
    """Sealos数据库连接帮助类"""
    
    def __init__(self):
        """初始化数据库连接参数"""
        self.config = {
            'host': os.getenv('MYSQL_HOST', 'your-sealos-host'),
            'port': int(os.getenv('MYSQL_PORT', '33949')),
            'user': os.getenv('MYSQL_USER', 'root'),
            'password': os.getenv('MYSQL_PASSWORD', ''),
            'database': os.getenv('MYSQL_NAME', 'your-database-name'),
            'charset': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
            'connect_timeout': int(os.getenv('MYSQL_CONNECT_TIMEOUT', '30')),
            'autocommit': True,
        }
    
    def test_connection(self):
        """
        测试数据库连接
        适合Codex环境初次部署时验证连接
        """
        try:
            print("🔍 测试Sealos数据库连接...")
            print(f"🌐 连接地址: {self.config['host']}:{self.config['port']}")
            
            connection = mysql.connector.connect(**self.config)
            
            if connection.is_connected():
                db_info = connection.get_server_info()
                print("✅ 成功连接到Sealos MySQL数据库!")
                print(f"📊 MySQL版本: {db_info}")
                
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                current_db = cursor.fetchone()
                print(f"🗄️  当前数据库: {current_db[0]}")
                
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
                print(f"📋 数据库表数量: {len(tables)}")
                
                cursor.close()
                connection.close()
                return True
                
        except Error as e:
            print(f"❌ 连接失败: {e}")
            print("💡 解决建议:")
            print("   1. 检查网络连接和代理配置")
            print("   2. 确认.env文件中的数据库配置正确")
            print("   3. 验证Sealos数据库服务是否正常运行")
            return False
    
    def get_django_db_config(self):
        """
        获取Django数据库配置
        返回适合Django DATABASES设置的字典
        """
        return {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': self.config['database'],
            'USER': self.config['user'],
            'PASSWORD': self.config['password'],
            'HOST': self.config['host'],
            'PORT': str(self.config['port']),
            'OPTIONS': {
                'charset': self.config['charset'],
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'connect_timeout': self.config['connect_timeout'],
            },
        }
    
    def create_database_if_not_exists(self, db_name=None):
        """
        创建数据库（如果不存在）
        适合Codex环境自动初始化
        """
        if not db_name:
            db_name = self.config['database']
            
        try:
            # 先连接到MySQL服务器（不指定数据库）
            temp_config = self.config.copy()
            del temp_config['database']
            
            connection = mysql.connector.connect(**temp_config)
            cursor = connection.cursor()
            
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 数据库 '{db_name}' 已创建或已存在")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:
            print(f"❌ 创建数据库失败: {e}")
            return False

def quick_test():
    """快速测试函数，适合Codex环境验证"""
    helper = SealosDBHelper()
    return helper.test_connection()

def get_env_template():
    """返回.env文件模板内容"""
    return """# ==========================================
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
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
TIME_ZONE=Asia/Shanghai
LANGUAGE_CODE=zh-hans"""

if __name__ == "__main__":
    print("🚀 Sealos数据库连接助手")
    print("=" * 40)
    
    # 检查环境变量
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_file):
        print("⚠️  未找到.env文件")
        print("📋 请创建.env文件，内容如下：")
        print(get_env_template())
        print("=" * 40)
    
    # 执行连接测试
    quick_test() 