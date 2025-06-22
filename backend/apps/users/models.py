from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid
import random
import string


class UserManager(BaseUserManager):
    """自定义用户管理器"""
    
    def create_user(self, phone, password=None, **extra_fields):
        """创建普通用户"""
        if not phone:
            raise ValueError('手机号是必需的')
        
        # 生成唯一标识号
        unique_identifier = self.model.generate_unique_identifier(phone)
        
        # 设置默认值
        extra_fields.setdefault('username', unique_identifier)
        extra_fields.setdefault('unique_identifier', unique_identifier)
        extra_fields.setdefault('nickname', unique_identifier)
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_phone_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置is_superuser=True')
        
        return self.create_user(phone, password, **extra_fields)


class BaseModel(models.Model):
    """
    基础模型类 - 为所有业务模型提供通用字段
    包含创建时间、更新时间、软删除等基础功能
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="主键ID")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    
    class Meta:
        abstract = True  # 抽象基类，不会在数据库中创建表


class User(AbstractUser, BaseModel):
    """
    扩展Django用户模型
    支持手机号注册，自动生成唯一标识号
    """
    # 手机号字段（主要登录方式）
    phone_validator = RegexValidator(
        regex=r'^1[3-9]\d{9}$',
        message="请输入正确的手机号码格式"
    )
    phone = models.CharField(
        max_length=11, 
        unique=True, 
        db_index=True,  # 显式索引优化查询性能
        validators=[phone_validator],
        verbose_name="手机号",
        help_text="用户的手机号，用于登录和验证"
    )
    
    # 用户唯一标识号（不可修改）
    unique_identifier = models.CharField(
        max_length=50, 
        unique=True, 
        editable=False,
        verbose_name="用户唯一标识",
        help_text="格式：uai{手机号}dx，dx为随机字符"
    )
    
    # 用户昵称（可修改）
    nickname = models.CharField(
        max_length=50, 
        verbose_name="用户昵称",
        help_text="用户可自定义的昵称，默认为唯一标识号"
    )
    
    # 邮箱设为可选
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")
    
    # 手机验证状态
    is_phone_verified = models.BooleanField(default=False, verbose_name="手机号是否已验证")
    
    # 注：add_time, update_time 由BaseModel提供，避免字段重复
    
    # 使用手机号作为用户名字段
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []  # 清空必填字段，UserManager会自动处理
    
    # 使用自定义用户管理器
    objects = UserManager()
    
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        db_table = "users_user"
    
    def save(self, *args, **kwargs):
        """
        重写save方法，自动生成唯一标识号和默认昵称
        """
        # 如果是新用户且没有唯一标识号，则生成
        if not self.unique_identifier and self.phone:
            self.unique_identifier = self.generate_unique_identifier(self.phone)
        
        # 如果没有昵称，使用唯一标识号作为默认昵称
        if not self.nickname:
            self.nickname = self.unique_identifier
            
        # 如果没有username，使用唯一标识号
        if not self.username:
            self.username = self.unique_identifier
            
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_identifier(phone):
        """
        生成用户唯一标识号：uai{手机号}dx
        dx为随机生成的2位英文字母（只能是字母，不能是数字）
        优化：批量生成候选避免频繁查询数据库
        """
        # 批量生成候选后缀，减少数据库查询次数
        candidates = [''.join(random.choices(string.ascii_lowercase, k=2)) for _ in range(10)]
        
        for suffix in candidates:
            unique_id = f"uai{phone}{suffix}"
            # 使用exists()进行轻量级存在性检查
            if not User.objects.filter(unique_identifier=unique_id).exists():
                return unique_id
        
        # 如果10个候选都重复，则回退到单次生成模式
        while True:
            random_suffix = ''.join(random.choices(string.ascii_lowercase, k=2))
            unique_id = f"uai{phone}{random_suffix}"
            if not User.objects.filter(unique_identifier=unique_id).exists():
                return unique_id
    
    def __str__(self):
        return f"{self.nickname}({self.phone})"


class UserProfile(BaseModel):
    """
    用户详细资料模型
    存储用户的扩展信息
    """
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="关联用户"
    )
    
    # 个人信息
    real_name = models.CharField(max_length=20, blank=True, verbose_name="真实姓名")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="性别")
    birth_date = models.DateField(blank=True, null=True, verbose_name="出生日期")
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, verbose_name="头像")
    
    # 联系信息
    qq = models.CharField(max_length=15, blank=True, verbose_name="QQ号")
    wechat = models.CharField(max_length=30, blank=True, verbose_name="微信号")
    
    # 地址信息
    province = models.CharField(max_length=20, blank=True, verbose_name="省份")
    city = models.CharField(max_length=20, blank=True, verbose_name="城市")
    address = models.CharField(max_length=100, blank=True, verbose_name="详细地址")
    
    # 个人简介
    bio = models.TextField(max_length=500, blank=True, verbose_name="个人简介")
    
    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"
        db_table = "users_profile"
    
    def __str__(self):
        return f"{self.user.nickname}的资料"


class WeChatBinding(BaseModel):
    """
    微信绑定模型
    管理用户的微信登录绑定信息
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='wechat_binding',
        verbose_name="关联用户"
    )
    
    # 微信相关信息
    openid = models.CharField(max_length=50, unique=True, verbose_name="微信OpenID")
    unionid = models.CharField(max_length=50, blank=True, verbose_name="微信UnionID")
    wechat_nickname = models.CharField(max_length=50, verbose_name="微信昵称")
    wechat_avatar = models.URLField(blank=True, verbose_name="微信头像URL")
    
    # 绑定状态
    is_bound = models.BooleanField(default=True, verbose_name="是否已绑定")
    bind_time = models.DateTimeField(auto_now_add=True, verbose_name="绑定时间")
    
    class Meta:
        verbose_name = "微信绑定"
        verbose_name_plural = "微信绑定"
        db_table = "users_wechat_binding"
    
    def __str__(self):
        return f"{self.user.nickname}的微信绑定"


class UserSetting(BaseModel):
    """
    用户设置模型
    存储用户的个性化设置
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='settings',
        verbose_name="关联用户"
    )
    
    # 通知设置
    email_notifications = models.BooleanField(default=True, verbose_name="邮件通知")
    sms_notifications = models.BooleanField(default=True, verbose_name="短信通知")
    wechat_notifications = models.BooleanField(default=True, verbose_name="微信通知")
    
    # 隐私设置
    profile_public = models.BooleanField(default=True, verbose_name="资料公开")
    learning_progress_public = models.BooleanField(default=False, verbose_name="学习进度公开")
    
    # 学习偏好
    preferred_language = models.CharField(
        max_length=10, 
        default='zh-cn', 
        verbose_name="首选语言",
        choices=[
            ('zh-cn', '简体中文'),
            ('zh-tw', '繁体中文'),
            ('en', 'English'),
        ]
    )
    
    # 其他设置（使用JSON字段存储灵活配置）
    extra_settings = models.JSONField(default=dict, blank=True, verbose_name="扩展设置")
    
    class Meta:
        verbose_name = "用户设置"
        verbose_name_plural = "用户设置"
        db_table = "users_settings"
    
    def __str__(self):
        return f"{self.user.nickname}的设置"


class LoginLog(BaseModel):
    """
    登录日志模型
    记录用户登录历史
    """
    LOGIN_TYPE_CHOICES = [
        ('phone_password', '手机密码登录'),
        ('phone_sms', '手机验证码登录'),
        ('wechat', '微信登录'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='login_logs',
        verbose_name="关联用户"
    )
    
    # 登录信息
    login_type = models.CharField(max_length=20, choices=LOGIN_TYPE_CHOICES, verbose_name="登录方式")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    user_agent = models.TextField(verbose_name="用户代理")
    
    # 登录结果
    is_success = models.BooleanField(default=True, verbose_name="是否成功")
    fail_reason = models.CharField(max_length=100, blank=True, verbose_name="失败原因")
    
    # 地理位置（可选）
    location = models.CharField(max_length=100, blank=True, verbose_name="登录地点")
    
    class Meta:
        verbose_name = "登录日志"
        verbose_name_plural = "登录日志"
        db_table = "users_login_log"
        ordering = ['-add_time']
        indexes = [
            models.Index(fields=['user', '-add_time'], name='idx_user_login_time'),
            models.Index(fields=['ip_address', '-add_time'], name='idx_ip_login_time'),
            models.Index(fields=['login_type', '-add_time'], name='idx_login_type_time'),
        ]
    
    def __str__(self):
        return f"{self.user.nickname} - {self.get_login_type_display()} - {self.add_time}"
