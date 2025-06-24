#!/usr/bin/env python3
"""
测试新的Sealos数据库连接
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def test_connection():
    """测试数据库连接"""
    print("🚀 测试Sealos数据库连接（端口48214）")
    print("="*50)
    
    # 加载环境变量
    load_dotenv()
    
    config = {
        'host': os.getenv('MYSQL_HOST'),
        'port': int(os.getenv('MYSQL_PORT')),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_NAME'),
        'charset': os.getenv('MYSQL_CHARSET', 'utf8mb4'),
        'connect_timeout': int(os.getenv('MYSQL_CONNECT_TIMEOUT', '120'))
    }
    
    print(f"📊 连接参数:")
    print(f"   主机: {config['host']}")
    print(f"   端口: {config['port']}")
    print(f"   用户: {config['user']}")
    print(f"   数据库: {config['database']}")
    print(f"   密码: {'*' * len(config['password'])}")
    print(f"   超时: {config['connect_timeout']}秒")
    
    try:
        print(f"\n🔌 正在连接...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ 数据库连接成功!")
            
            cursor = connection.cursor()
            
            # 获取MySQL版本
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   📊 MySQL版本: {version[0]}")
            
            # 获取当前数据库
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"   🗄️  当前数据库: {db[0]}")
            
            # 测试基本操作
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   📋 数据库表数量: {len(tables)}")
            
            if tables:
                print(f"   📋 现有表: {[table[0] for table in tables[:5]]}")
            else:
                print("   📋 数据库为空，准备Django迁移")
            
            # 测试权限
            cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
            grants = cursor.fetchall()
            print(f"   🔐 用户权限: 已获取{len(grants)}项权限")
            
            cursor.close()
            connection.close()
            
            print(f"\n🎉 数据库连接测试完全成功!")
            print(f"✅ 可以进行Django迁移和开发")
            return True
            
    except Error as e:
        print(f"❌ 连接失败: {e}")
        print(f"\n💡 故障排除建议:")
        
        if "1045" in str(e):
            print("   - 检查用户名和密码是否正确")
            print("   - 确认用户具有远程连接权限")
        elif "2003" in str(e):
            print("   - 检查主机地址和端口号")
            print("   - 确认防火墙允许连接")
        elif "2005" in str(e):
            print("   - 检查域名解析")
            print("   - 确认网络连接正常")
        else:
            print("   - 检查所有连接参数")
            print("   - 联系Sealos技术支持")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    
    if success:
        print(f"\n🚀 下一步操作:")
        print(f"1. 运行Django迁移: python manage.py migrate")
        print(f"2. 创建超级用户: python manage.py createsuperuser")
        print(f"3. 启动服务器: python manage.py runserver")
    else:
        print(f"\n⚠️  请先解决连接问题再继续") 