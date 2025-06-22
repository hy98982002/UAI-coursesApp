#!/usr/bin/env python
"""
UAI教育平台用户系统测试脚本
演示用户注册、唯一标识生成等核心功能
"""

import os
import sys
import django

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uai_backend.settings')
django.setup()

from apps.users.models import User, UserProfile, WeChatBinding


def test_user_creation():
    """测试用户创建和唯一标识生成"""
    print("=" * 50)
    print("🧪 测试用户创建和唯一标识生成")
    print("=" * 50)
    
    # 测试数据
    test_phones = [
        "18512291362",
        "13888888888", 
        "15999999999",
    ]
    
    for phone in test_phones:
        try:
            # 删除已存在的用户（如果有）
            if User.objects.filter(phone=phone).exists():
                User.objects.filter(phone=phone).delete()
                print(f"🗑️  删除已存在的用户: {phone}")
            
            # 创建新用户
            user = User.objects.create_user(
                phone=phone,
                password='test123456'
            )
            
            print(f"✅ 创建用户成功:")
            print(f"   📱 手机号: {user.phone}")
            print(f"   🔑 唯一标识: {user.unique_identifier}")
            print(f"   😊 昵称: {user.nickname}")
            print(f"   📅 注册时间: {user.add_time}")
            print(f"   ✅ 手机验证: {user.is_phone_verified}")
            
            # 检查自动创建的Profile和Setting
            if hasattr(user, 'profile'):
                print(f"   📝 Profile已创建: ID={user.profile.id}")
            if hasattr(user, 'settings'):
                print(f"   ⚙️  Settings已创建: 语言={user.settings.preferred_language}")
            
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ 创建用户失败 {phone}: {str(e)}")


def test_unique_identifier_generation():
    """测试唯一标识符生成的唯一性"""
    print("\n" + "=" * 50)
    print("🧪 测试唯一标识符唯一性")
    print("=" * 50)
    
    phone = "13700000000"
    identifiers = set()
    
    # 生成10个标识符，测试唯一性
    for i in range(10):
        identifier = User.generate_unique_identifier(phone)
        identifiers.add(identifier)
        print(f"第{i+1}个标识: {identifier}")
    
    print(f"\n生成了 {len(identifiers)} 个唯一标识（应该是10个）")
    print(f"唯一性测试: {'✅ 通过' if len(identifiers) == 10 else '❌ 失败'}")


def test_wechat_binding():
    """测试微信绑定功能"""
    print("\n" + "=" * 50)
    print("🧪 测试微信绑定功能")
    print("=" * 50)
    
    try:
        # 获取一个测试用户
        user = User.objects.filter(phone="18512291362").first()
        if not user:
            print("❌ 未找到测试用户，请先运行用户创建测试")
            return
        
        # 创建微信绑定
        wechat_binding = WeChatBinding.objects.create(
            user=user,
            openid="mock_openid_123456",
            wechat_nickname="测试微信用户",
            wechat_avatar="https://example.com/avatar.jpg"
        )
        
        print(f"✅ 微信绑定成功:")
        print(f"   👤 用户: {user.nickname}")
        print(f"   🆔 OpenID: {wechat_binding.openid}")
        print(f"   😊 微信昵称: {wechat_binding.wechat_nickname}")
        print(f"   🔗 绑定状态: {wechat_binding.is_bound}")
        print(f"   📅 绑定时间: {wechat_binding.bind_time}")
        
    except Exception as e:
        print(f"❌ 微信绑定失败: {str(e)}")


def test_user_profile_update():
    """测试用户资料更新"""
    print("\n" + "=" * 50)
    print("🧪 测试用户资料更新")
    print("=" * 50)
    
    try:
        user = User.objects.filter(phone="18512291362").first()
        if not user:
            print("❌ 未找到测试用户")
            return
        
        # 更新用户基本信息
        user.nickname = "UAI学习者"
        user.email = "test@example.com"
        user.save()
        
        # 更新用户详细资料
        profile = user.profile
        profile.real_name = "张同学"
        profile.gender = "M"
        profile.city = "北京"
        profile.bio = "热爱学习的程序员"
        profile.save()
        
        print(f"✅ 用户资料更新成功:")
        print(f"   📱 手机号: {user.phone}")
        print(f"   🔑 唯一标识: {user.unique_identifier}")
        print(f"   😊 昵称: {user.nickname}")
        print(f"   📧 邮箱: {user.email}")
        print(f"   👤 真实姓名: {profile.real_name}")
        print(f"   👥 性别: {profile.get_gender_display()}")
        print(f"   🏙️  城市: {profile.city}")
        print(f"   📝 简介: {profile.bio}")
        
    except Exception as e:
        print(f"❌ 资料更新失败: {str(e)}")


def display_summary():
    """显示测试总结"""
    print("\n" + "=" * 50)
    print("📊 测试总结")
    print("=" * 50)
    
    total_users = User.objects.count()
    total_profiles = UserProfile.objects.count()
    total_wechat_bindings = WeChatBinding.objects.count()
    
    print(f"👥 总用户数: {total_users}")
    print(f"📝 总资料数: {total_profiles}")
    print(f"💬 微信绑定数: {total_wechat_bindings}")
    
    print("\n📋 用户列表:")
    for user in User.objects.all():
        wechat_status = "已绑定" if hasattr(user, 'wechat_binding') and user.wechat_binding.is_bound else "未绑定"
        print(f"   📱 {user.phone} | 🔑 {user.unique_identifier} | 😊 {user.nickname} | 💬 {wechat_status}")


if __name__ == "__main__":
    print("🚀 开始UAI教育平台用户系统测试")
    
    try:
        # 执行各项测试
        test_user_creation()
        test_unique_identifier_generation()
        test_wechat_binding()
        test_user_profile_update()
        display_summary()
        
        print("\n🎉 所有测试完成!")
        
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50) 