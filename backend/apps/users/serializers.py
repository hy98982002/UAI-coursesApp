from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, WeChatBinding, UserSetting
from .utils import SmsCodeManager, is_valid_phone


class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'confirm_password', 'nickname')
        extra_kwargs = {
            'nickname': {'required': False}
        }
    
    def validate(self, attrs):
        """验证密码一致性"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return attrs
    
    def validate_phone(self, value):
        """验证手机号唯一性"""
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号已注册")
        return value
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    phone = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        """验证用户登录"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        if phone and password:
            # 先查找用户是否存在
            try:
                user = User.objects.get(phone=phone)
                
                # 检查用户是否设置了密码
                if not user.has_usable_password():
                    raise serializers.ValidationError('当前用户未设置密码，请使用验证码登录')
                
                # 验证密码
                user = authenticate(request=self.context.get('request'),
                                  username=phone, password=password)
                
                if not user:
                    raise serializers.ValidationError('手机号或密码错误')
                
                if not user.is_active:
                    raise serializers.ValidationError('用户账号已被禁用')
                    
                attrs['user'] = user
                return attrs
            except User.DoesNotExist:
                raise serializers.ValidationError('该手机号未注册')
        else:
            raise serializers.ValidationError('必须输入手机号和密码')


class SMSLoginSerializer(serializers.Serializer):
    """短信验证码登录序列化器"""
    phone = serializers.CharField()
    sms_code = serializers.CharField(max_length=6)
    
    def validate_phone(self, value):
        """验证手机号格式"""
        if not is_valid_phone(value):
            raise serializers.ValidationError('请输入正确的手机号格式')
        return value
    
    def validate(self, attrs):
        """验证短信验证码"""
        phone = attrs.get('phone')
        sms_code = attrs.get('sms_code')
        
        # 使用验证码管理器验证
        verification_result = SmsCodeManager.verify_code(phone, sms_code, 'login')
        
        if not verification_result['valid']:
            raise serializers.ValidationError(verification_result['message'])
        
        # 检查用户是否存在，不存在则自动注册
        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={
                'is_phone_verified': False  # 注册时先不验证，等验证码通过再标记
            }
        )
        
        # 验证码验证通过后，标记手机号已验证
        if not user.is_phone_verified:
            user.is_phone_verified = True
            user.save(update_fields=['is_phone_verified'])
        
        attrs['user'] = user
        return attrs


class SMSRegistrationSerializer(serializers.Serializer):
    """短信验证码注册序列化器"""
    phone = serializers.CharField()
    sms_code = serializers.CharField(max_length=6)
    
    def validate_phone(self, value):
        """验证手机号格式和唯一性"""
        if not is_valid_phone(value):
            raise serializers.ValidationError('请输入正确的手机号格式')
        
        # 检查手机号是否已注册
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('该手机号已注册，请直接登录')
        
        return value
    
    def validate(self, attrs):
        """验证短信验证码"""
        phone = attrs.get('phone')
        sms_code = attrs.get('sms_code')
        
        # 使用验证码管理器验证
        verification_result = SmsCodeManager.verify_code(phone, sms_code, 'register')
        
        if not verification_result['valid']:
            raise serializers.ValidationError(verification_result['message'])
        
        return attrs
    
    def create(self, validated_data):
        """创建用户（不设置密码）"""
        phone = validated_data.get('phone')
        
        # 创建用户，明确设置为不可用密码
        user = User.objects.create(
            phone=phone,
            is_phone_verified=True,  # 验证码验证通过，标记手机号已验证
        )
        
        # 明确设置为不可用密码状态
        user.set_unusable_password()
        user.save()
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """用户资料序列化器"""
    user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'real_name',
            'gender',
            'birth_date',
            'avatar',
            'qq',
            'wechat',
            'province',
            'city',
            'address',
            'bio',
            'is_active',
            'add_time',
            'update_time',
            'user_info',
        )
        read_only_fields = ('user', 'add_time', 'update_time')
    
    def get_user_info(self, obj):
        """获取关联用户基本信息"""
        return {
            'phone': obj.user.phone,
            'unique_identifier': obj.user.unique_identifier,
            'nickname': obj.user.nickname,
            'is_phone_verified': obj.user.is_phone_verified,
        }


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""
    profile = UserProfileSerializer(read_only=True)
    wechat_binding = serializers.SerializerMethodField()
    has_wechat = serializers.SerializerMethodField()
    has_password = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('phone', 'unique_identifier', 'nickname', 'email', 
                 'is_phone_verified', 'add_time', 'profile', 
                 'wechat_binding', 'has_wechat', 'has_password')
        read_only_fields = ('phone', 'unique_identifier', 'add_time', 'is_phone_verified')
    
    def get_wechat_binding(self, obj):
        """获取微信绑定信息"""
        try:
            binding = obj.wechat_binding
            return {
                'is_bound': binding.is_bound,
                'wechat_nickname': binding.wechat_nickname,
                'bind_time': binding.bind_time
            }
        except WeChatBinding.DoesNotExist:
            return None
    
    def get_has_wechat(self, obj):
        """是否已绑定微信"""
        try:
            return obj.wechat_binding.is_bound
        except WeChatBinding.DoesNotExist:
            return False
    
    def get_has_password(self, obj):
        """是否已设置密码"""
        return obj.has_usable_password()


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(
        required=False,  # 允许为空，让首次设置密码可以不传
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        user = self.context["request"].user
        old_pwd = attrs.get("old_password")
        new_pwd = attrs["new_password"]
        confirm_pwd = attrs["confirm_password"]

        # 🔍 添加调试信息
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"用户 {user.phone} 设置密码 - has_usable_password: {user.has_usable_password()}")
        logger.info(f"用户密码字段: {repr(user.password)}")

        # 1️⃣ 两次新密码一致性
        if new_pwd != confirm_pwd:
            raise serializers.ValidationError({"confirm_password": "两次密码不一致"})

        # 2️⃣ 仅当用户"已经有可用密码"时才校验旧密码
        if user.has_usable_password():
            logger.info(f"用户 {user.phone} 已有密码，要求提供旧密码")
            if not old_pwd:
                raise serializers.ValidationError({"old_password": "旧密码必填"})
            if not user.check_password(old_pwd):
                raise serializers.ValidationError({"old_password": "旧密码错误"})
            
            # 防止密码重用
            if user.check_password(new_pwd):
                raise serializers.ValidationError({"new_password": "新密码不能与旧密码相同"})
        else:
            logger.info(f"用户 {user.phone} 首次设置密码，跳过旧密码验证")

        # 3️⃣ 结合 Django 自带密码强度校验
        validate_password(new_pwd, user=user)

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()

        # 返回新的 JWT，方便前端自动替换
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }


class WeChatBindingSerializer(serializers.ModelSerializer):
    """微信绑定序列化器"""
    
    class Meta:
        model = WeChatBinding
        fields = ('openid', 'wechat_nickname', 'wechat_avatar', 'is_bound', 'bind_time')
        read_only_fields = ('bind_time',)


class UserSettingSerializer(serializers.ModelSerializer):
    """用户设置序列化器"""
    
    class Meta:
        model = UserSetting
        fields = (
            'id',
            'user',
            'email_notifications',
            'sms_notifications',
            'wechat_notifications',
            'profile_public',
            'learning_progress_public',
            'preferred_language',
            'extra_settings',
            'is_active',
            'add_time',
            'update_time',
        )
        read_only_fields = ('user', 'add_time', 'update_time') 