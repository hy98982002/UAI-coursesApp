#!/usr/bin/env python
"""
测试用户唯一标识符生成逻辑
验证后缀只包含英文字母作为后缀
"""

import os
import sys
import django
import re

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uai_backend.settings')
django.setup()

from apps.users.models import User


def test_identifier_letters_only():
    """测试唯一标识符后缀只包含英文字母"""
    print("=" * 60)
    print("🧪 测试唯一标识符后缀只包含英文字母")
    print("=" * 60)
    
    test_phone = "13800138000"
    
    # 生成50个标识符进行测试
    identifiers = []
    for i in range(50):
        identifier = User.generate_unique_identifier(test_phone)
        identifiers.append(identifier)
        
        # 验证格式：uai + 手机号 + 2位英文字母
        pattern = r'^uai13800138000[a-z]{2}$'
        is_valid = bool(re.match(pattern, identifier))
        
        status = "✅" if is_valid else "❌"
        print(f"{status} 第{i+1:2d}个: {identifier} - {'格式正确' if is_valid else '格式错误'}")
        
        if not is_valid:
            print(f"❌ 错误: 标识符 {identifier} 不符合要求!")
            return False
    
    # 检查唯一性
    unique_count = len(set(identifiers))
    print(f"\n📊 测试统计:")
    print(f"   🎯 生成总数: {len(identifiers)}")
    print(f"   🔑 唯一个数: {unique_count}")
    print(f"   ✅ 唯一性: {'通过' if unique_count == len(identifiers) else '失败'}")
    
    # 验证后缀字符
    all_suffixes = [id[-2:] for id in identifiers]
    all_chars = set(''.join(all_suffixes))
    
    print(f"\n🔤 后缀字符分析:")
    print(f"   📝 使用的字符: {sorted(all_chars)}")
    print(f"   🔢 是否包含数字: {'是' if any(c.isdigit() for c in all_chars) else '否'}")
    print(f"   🔤 是否只有字母: {'是' if all(c.isalpha() and c.islower() for c in all_chars) else '否'}")
    
    # 最终验证
    is_all_letters = all(c.isalpha() and c.islower() for c in all_chars)
    has_no_digits = not any(c.isdigit() for c in all_chars)
    
    if is_all_letters and has_no_digits:
        print(f"\n🎉 测试结果: ✅ 通过")
        print(f"   ✅ 所有后缀都只包含小写英文字母")
        print(f"   ✅ 没有包含任何数字")
        return True
    else:
        print(f"\n💥 测试结果: ❌ 失败")
        print(f"   ❌ 后缀包含了非字母字符")
        return False


def test_new_user_creation():
    """测试创建新用户的标识符"""
    print("\n" + "=" * 60)
    print("🧪 测试新用户创建的标识符格式")
    print("=" * 60)
    
    test_phones = [
        "15800000001",
        "15800000002", 
        "15800000003"
    ]
    
    created_users = []
    
    for phone in test_phones:
        try:
            # 删除已存在的用户
            User.objects.filter(phone=phone).delete()
            
            # 创建新用户
            user = User.objects.create_user(
                phone=phone,
                password='test123456'
            )
            
            created_users.append(user)
            
            # 验证标识符格式
            pattern = rf'^uai{phone}[a-z]{{2}}$'
            is_valid = bool(re.match(pattern, user.unique_identifier))
            
            status = "✅" if is_valid else "❌"
            print(f"{status} 用户: {phone}")
            print(f"   🔑 标识符: {user.unique_identifier}")
            print(f"   📝 后缀: {user.unique_identifier[-2:]}")
            print(f"   ✅ 格式正确: {'是' if is_valid else '否'}")
            print("-" * 40)
            
        except Exception as e:
            print(f"❌ 创建用户失败 {phone}: {str(e)}")
    
    return created_users


def main():
    """主测试函数"""
    print("🚀 开始测试唯一标识符英文字母限制")
    
    try:
        # 测试标识符生成逻辑
        result1 = test_identifier_letters_only()
        
        # 测试用户创建
        users = test_new_user_creation()
        
        print("\n" + "=" * 60)
        print("📋 测试总结")
        print("=" * 60)
        
        if result1:
            print("✅ 标识符生成逻辑测试: 通过")
        else:
            print("❌ 标识符生成逻辑测试: 失败")
        
        print(f"✅ 用户创建测试: 成功创建 {len(users)} 个用户")
        
        # 显示所有用户的标识符
        print(f"\n📋 当前数据库中的用户标识符:")
        all_users = User.objects.all()
        for user in all_users:
            suffix = user.unique_identifier[-2:]
            has_digits = any(c.isdigit() for c in suffix)
            status = "❌数字" if has_digits else "✅字母"
            print(f"   📱 {user.phone} | 🔑 {user.unique_identifier} | {status}")
        
        print(f"\n🎉 测试完成!")
        
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 