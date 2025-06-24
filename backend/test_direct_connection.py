#!/usr/bin/env python3
"""
直接测试Sealos数据库连接（避免缓存问题）
"""

import mysql.connector
from mysql.connector import Error

def test_direct_connection():
    """直接测试数据库连接"""
    print("🚀 直接测试Sealos数据库连接")
    print("="*50)
    
    # 直接使用提供的连接信息
    config = {
        'host': 'dbconn.sealosbja.site',
        'port': 48214,
        'user': 'root',
        'password': '4mhpzmwn',
        'database': 'test-db-mysql-0',
        'charset': 'utf8mb4',
        'connect_timeout': 120
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
            try:
                cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
                grants = cursor.fetchall()
                print(f"   🔐 用户权限: 已获取{len(grants)}项权限")
            except Error as e:
                print(f"   🔐 权限检查: {e}")
            
            # 测试创建表的权限
            try:
                cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY)")
                cursor.execute("DROP TABLE IF EXISTS test_table")
                print(f"   ✅ 创建/删除表权限: 正常")
            except Error as e:
                print(f"   ⚠️  表操作权限: {e}")
            
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
    success = test_direct_connection()
    
    if success:
        print(f"\n🚀 下一步操作:")
        print(f"1. 运行Django数据库检查: python manage.py check --database default")
        print(f"2. 运行Django迁移: python manage.py migrate")
        print(f"3. 创建超级用户: python manage.py createsuperuser")
        print(f"4. 启动服务器: python manage.py runserver")
        print(f"\n📝 连接字符串: mysql://root:4mhpzmwn@dbconn.sealosbja.site:48214/test-db-mysql-0")
    else:
        print(f"\n⚠️  请先解决连接问题再继续") 