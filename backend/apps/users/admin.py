from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, WeChatBinding, UserSetting, LoginLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ('phone', 'unique_identifier', 'nickname', 'is_phone_verified', 
                    'is_active', 'is_staff', 'add_time')
    list_filter = ('is_phone_verified', 'is_active', 'is_staff', 'add_time')
    search_fields = ('phone', 'unique_identifier', 'nickname', 'email')
    ordering = ('-add_time',)
    
    # 性能优化
    list_select_related = ('profile',)  # 预加载关联对象
    raw_id_fields = ('groups', 'user_permissions')  # 大数据量字段使用原始ID选择器
    list_per_page = 50  # 分页优化
    
    # 详情页面字段组织
    fieldsets = (
        ('基本信息', {
            'fields': ('phone', 'unique_identifier', 'nickname', 'email')
        }),
        ('权限信息', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_phone_verified')
        }),
        ('重要日期', {
            'fields': ('last_login', 'date_joined', 'add_time')
        }),
        ('用户组', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )
    
    # 添加用户时的字段
    add_fieldsets = (
        ('创建新用户', {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'nickname'),
        }),
    )
    
    readonly_fields = ('unique_identifier', 'add_time', 'date_joined', 'last_login')
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时使唯一标识号只读"""
        if obj:  # 编辑现有用户
            return self.readonly_fields + ('phone',)
        return self.readonly_fields


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理"""
    list_display = ('user', 'real_name', 'gender', 'city', 'add_time')
    list_filter = ('gender', 'province', 'add_time')
    search_fields = ('user__phone', 'user__nickname', 'real_name', 'city')
    ordering = ('-add_time',)
    
    # 性能优化
    list_select_related = ('user',)  # 预加载用户对象
    list_per_page = 50
    
    fieldsets = (
        ('关联用户', {
            'fields': ('user',)
        }),
        ('个人信息', {
            'fields': ('real_name', 'gender', 'birth_date', 'avatar')
        }),
        ('联系方式', {
            'fields': ('qq', 'wechat')
        }),
        ('地址信息', {
            'fields': ('province', 'city', 'address')
        }),
        ('个人简介', {
            'fields': ('bio',)
        }),
    )
    
    def avatar_preview(self, obj):
        """头像预览"""
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)
        return "无头像"
    avatar_preview.short_description = "头像预览"


@admin.register(WeChatBinding)
class WeChatBindingAdmin(admin.ModelAdmin):
    """微信绑定管理"""
    list_display = ('user', 'wechat_nickname', 'is_bound', 'bind_time')
    list_filter = ('is_bound', 'bind_time')
    search_fields = ('user__phone', 'user__nickname', 'wechat_nickname', 'openid')
    ordering = ('-bind_time',)
    
    fieldsets = (
        ('关联用户', {
            'fields': ('user',)
        }),
        ('微信信息', {
            'fields': ('openid', 'unionid', 'wechat_nickname', 'wechat_avatar')
        }),
        ('绑定状态', {
            'fields': ('is_bound', 'bind_time')
        }),
    )
    
    readonly_fields = ('bind_time',)
    
    def wechat_avatar_preview(self, obj):
        """微信头像预览"""
        if obj.wechat_avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.wechat_avatar)
        return "无头像"
    wechat_avatar_preview.short_description = "微信头像"


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    """用户设置管理"""
    list_display = ('user', 'preferred_language', 'email_notifications', 
                    'sms_notifications', 'profile_public')
    list_filter = ('preferred_language', 'email_notifications', 'sms_notifications', 
                   'profile_public', 'learning_progress_public')
    search_fields = ('user__phone', 'user__nickname')
    
    fieldsets = (
        ('关联用户', {
            'fields': ('user',)
        }),
        ('通知设置', {
            'fields': ('email_notifications', 'sms_notifications', 'wechat_notifications')
        }),
        ('隐私设置', {
            'fields': ('profile_public', 'learning_progress_public')
        }),
        ('偏好设置', {
            'fields': ('preferred_language',)
        }),
        ('扩展设置', {
            'fields': ('extra_settings',),
            'classes': ('collapse',)
        }),
    )


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """登录日志管理"""
    list_display = ('user', 'login_type', 'ip_address', 'is_success', 'location', 'add_time')
    list_filter = ('login_type', 'is_success', 'add_time')
    search_fields = ('user__phone', 'user__nickname', 'ip_address', 'location')
    ordering = ('-add_time',)
    
    # 性能优化和用户体验提升
    list_select_related = ('user',)  # 预加载用户对象
    date_hierarchy = 'add_time'  # 按日期分层浏览，方便检索
    list_per_page = 100  # 日志数据可以多显示一些
    
    fieldsets = (
        ('用户信息', {
            'fields': ('user',)
        }),
        ('登录信息', {
            'fields': ('login_type', 'ip_address', 'user_agent', 'location')
        }),
        ('登录结果', {
            'fields': ('is_success', 'fail_reason')
        }),
        ('时间信息', {
            'fields': ('add_time',)
        }),
    )
    
    readonly_fields = ('add_time',)
    
    # 禁止添加和编辑，这是系统自动记录的日志
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # 只有超级用户可删除日志


# 自定义管理后台标题
admin.site.site_header = 'UAI教育平台管理后台'
admin.site.site_title = 'UAI管理'
admin.site.index_title = '欢迎使用UAI教育平台管理系统'
