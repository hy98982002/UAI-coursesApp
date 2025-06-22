from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

# 创建DRF路由器
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')

app_name = 'users'

urlpatterns = [
    # 认证相关API
    path('auth/register/', views.register_view, name='register'),
    path('auth/sms-register/', views.sms_register_view, name='sms_register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/sms-login/', views.sms_login_view, name='sms_login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/send-sms/', views.send_sms_code_view, name='send_sms'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户管理API (通过ViewSet提供)
    path('', include(router.urls)),
]

"""
用户模块API路由说明：

认证相关：
- POST /api/users/auth/register/         - 用户注册（需要密码）
- POST /api/users/auth/sms-register/     - 短信验证码注册（不需要密码）
- POST /api/users/auth/login/           - 密码登录  
- POST /api/users/auth/sms-login/       - 验证码登录
- POST /api/users/auth/logout/          - 用户登出
- POST /api/users/auth/send-sms/        - 发送验证码
- POST /api/users/auth/refresh/         - 刷新Token

用户管理：
- GET  /api/users/user/profile/         - 获取用户信息
- PUT  /api/users/user/update_profile/  - 更新基本信息
- PUT  /api/users/user/update_user_profile/ - 更新详细资料
- POST /api/users/user/change_password/ - 修改密码
- GET  /api/users/user/settings/        - 获取用户设置
- PUT  /api/users/user/update_settings/ - 更新用户设置
""" 