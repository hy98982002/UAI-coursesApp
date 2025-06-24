#!/usr/bin/env python3
"""
连接MySQL服务器并列出所有可用的数据库
"""

import mysql.connector
from mysql.connector import Error

def test_and_list_databases():
    """连接MySQL服务器并列出数据库"""
    print("🚀 连接MySQL服务器并查看可用数据库")
    print("="*50)
    
    # 不指定数据库名称，先连接到MySQL服务器
    config = {
        'host': 'dbconn.sealosbja.site',
        'port': 48214,
        'user': 'root',
        'password': '4mhpzmwn',
        'charset': 'utf8mb4',
        'connect_timeout': 120
    }
    
    print(f"📊 连接参数:")
    print(f"   主机: {config['host']}")
    print(f"   端口: {config['port']}")
    print(f"   用户: {config['user']}")
    print(f"   密码: {'*' * len(config['password'])}")
    
    try:
        print(f"\n🔌 正在连接MySQL服务器...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ MySQL服务器连接成功!")
            
            cursor = connection.cursor()
            
            # 获取MySQL版本
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   📊 MySQL版本: {version[0]}")
            
            # 列出所有数据库
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"\n📋 可用数据库列表:")
            for i, db in enumerate(databases, 1):
                db_name = db[0]
                print(f"   {i}. {db_name}")
                
                # 跳过系统数据库，检查用户数据库
                if db_name not in ['information_schema', 'mysql', 'performance_schema', 'sys']:
                    print(f"      👆 这可能是您的数据库!")
            
            # 查看当前用户权限
            cursor.execute("SELECT USER(), CURRENT_USER()")
            user_info = cursor.fetchone()
            print(f"\n🔐 用户信息:")
            print(f"   当前用户: {user_info[0]}")
            print(f"   认证用户: {user_info[1]}")
            
            cursor.close()
            connection.close()
            
            print(f"\n🎉 服务器连接成功!")
            
            # 给出建议的数据库名称
            user_databases = [db[0] for db in databases if db[0] not in ['information_schema', 'mysql', 'performance_schema', 'sys']]
            
            if user_databases:
                suggested_db = user_databases[0]
                print(f"\n💡 建议使用的数据库: {suggested_db}")
                print(f"📝 更新.env文件:")
                print(f"   MYSQL_NAME={suggested_db}")
                
                # 尝试连接到建议的数据库
                return test_specific_database(suggested_db)
            else:
                print(f"\n⚠️  没有找到用户数据库，可能需要创建")
                return False
            
    except Error as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_specific_database(db_name):
    """测试连接到特定数据库"""
    print(f"\n🔍 测试连接到数据库: {db_name}")
    
    config = {
        'host': 'dbconn.sealosbja.site',
        'port': 48214,
        'user': 'root',
        'password': '4mhpzmwn',
        'database': db_name,
        'charset': 'utf8mb4',
        'connect_timeout': 120
    }
    
    try:
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print(f"✅ 成功连接到数据库: {db_name}")
            
            cursor = connection.cursor()
            
            # 查看数据库中的表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   📋 数据库表数量: {len(tables)}")
            
            if tables:
                print(f"   📋 现有表: {[table[0] for table in tables]}")
            else:
                print("   📋 数据库为空，准备Django迁移")
            
            cursor.close()
            connection.close()
            
            return True
            
    except Error as e:
        print(f"❌ 连接数据库失败: {e}")
        return False

if __name__ == "__main__":
    success = test_and_list_databases()
    
    if success:
        print(f"\n🚀 下一步操作:")
        print(f"1. 更新backend/.env文件中的MYSQL_NAME")
        print(f"2. 运行Django迁移: python manage.py migrate")
        print(f"3. 创建超级用户: python manage.py createsuperuser")
        print(f"4. 启动服务器: python manage.py runserver")
    else:
        print(f"\n⚠️  请检查数据库配置") 