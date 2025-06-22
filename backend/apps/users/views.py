from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.throttling import UserRateThrottle
from .throttles import ChangePwdThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import transaction
import logging

from .models import User, UserProfile, LoginLog
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, SMSLoginSerializer,
    UserDetailSerializer, UserProfileSerializer, ChangePasswordSerializer,
    WeChatBindingSerializer, UserSettingSerializer, SMSRegistrationSerializer
)
from .utils import SmsCodeManager, is_valid_phone, format_phone_number

logger = logging.getLogger('apps.users')


def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_login_log(user, request, login_type, is_success=True, fail_reason=''):
    """创建登录日志"""
    LoginLog.objects.create(
        user=user,
        login_type=login_type,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        is_success=is_success,
        fail_reason=fail_reason
    )


def get_tokens_for_user(user):
    """为用户生成JWT令牌"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """
    用户注册API
    POST /api/auth/register/
    """
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # 生成JWT令牌
            tokens = get_tokens_for_user(user)
            
            # 记录注册成功日志
            logger.info(f"用户注册成功: {user.phone}")
            
            return Response({
                'status': 201,
                'msg': '注册成功',
                'data': {
                    'user': UserDetailSerializer(user).data,
                    'tokens': tokens
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"用户注册失败: {str(e)}")
            return Response({
                'status': 500,
                'msg': '注册失败，请稍后重试',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 400,
        'msg': '注册信息有误',
        'data': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    密码登录API
    POST /api/auth/login/
    """
    serializer = UserLoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # 生成JWT令牌
        tokens = get_tokens_for_user(user)
        
        # 记录登录日志
        create_login_log(user, request, 'phone_password', True)
        
        logger.info(f"用户登录成功: {user.phone}")
        
        return Response({
            'status': 200,
            'msg': '登录成功',
            'data': {
                'user': UserDetailSerializer(user).data,
                'tokens': tokens
            }
        })
    
    # 记录登录失败日志
    phone = request.data.get('phone', '')
    if phone:
        try:
            user = User.objects.get(phone=phone)
            create_login_log(user, request, 'phone_password', False, '密码错误')
        except User.DoesNotExist:
            pass
    
    return Response({
        'status': 401,
        'msg': '登录失败',
        'data': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sms_login_view(request):
    """
    短信验证码登录API
    POST /api/auth/sms-login/
    """
    serializer = SMSLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # 生成JWT令牌
        tokens = get_tokens_for_user(user)
        
        # 记录登录日志
        create_login_log(user, request, 'phone_sms', True)
        
        logger.info(f"用户短信登录成功: {user.phone}")
        
        return Response({
            'status': 200,
            'msg': '登录成功',
            'data': {
                'user': UserDetailSerializer(user).data,
                'tokens': tokens
            }
        })
    
    return Response({
        'status': 401,
        'msg': '登录失败',
        'data': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_sms_code_view(request):
    """
    发送短信验证码API
    POST /api/auth/send-sms/
    """
    phone = request.data.get('phone', '')
    code_type = request.data.get('code_type', 'default')  # register, login, reset_password等
    
    # 验证手机号格式
    if not is_valid_phone(phone):
        logger.warning(f"手机号格式错误: {phone}")
        return Response({
            'status': 400,
            'msg': '请输入正确的手机号格式',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # 检查发送频率限制
    send_check = SmsCodeManager.can_send_code(phone)
    if not send_check['can_send']:
        logger.warning(f"验证码发送频率超限: {format_phone_number(phone)}")
        return Response({
            'status': 429,
            'msg': send_check['message'],
            'data': None
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    try:
        # 生成验证码
        code = SmsCodeManager.generate_code()
        
        # 开发环境使用固定验证码
        if hasattr(SmsCodeManager, 'get_development_code'):
            dev_code = SmsCodeManager.get_development_code()
            if dev_code:
                code = dev_code
        
        # 存储验证码
        if not SmsCodeManager.store_code(phone, code, code_type):
            logger.error(f"验证码存储失败: {format_phone_number(phone)}")
            return Response({
                'status': 500,
                'msg': '验证码发送失败，请稍后重试',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 记录发送次数
        SmsCodeManager.record_send(phone)
        
        # TODO: 实际项目中这里应该集成真实的短信服务
        # 现在暂时在日志中显示验证码用于测试
        logger.info(f"发送短信验证码到: {format_phone_number(phone)}, 验证码: {code}")
        
        return Response({
            'status': 200,
            'msg': '验证码发送成功',
            'data': {
                'phone': format_phone_number(phone),
                'expire_minutes': SmsCodeManager.CODE_EXPIRE_MINUTES,
                'remaining_count': send_check.get('remaining_count', 0) - 1
            }
        })
        
    except Exception as e:
        logger.error(f"发送验证码异常: {format_phone_number(phone)} - {str(e)}")
        return Response({
            'status': 500,
            'msg': '验证码发送失败，请稍后重试',
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def sms_register_view(request):
    """
    短信验证码注册API
    POST /api/auth/sms-register/
    """
    serializer = SMSRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            user = serializer.save()
            
            # 生成JWT令牌
            tokens = get_tokens_for_user(user)
            
            # 记录注册成功日志
            logger.info(f"用户短信注册成功: {user.phone}")
            
            return Response({
                'status': 201,
                'msg': '注册成功！建议您前往个人中心设置登录密码以提高账户安全性。',
                'data': {
                    'user': UserDetailSerializer(user).data,
                    'tokens': tokens,
                    'need_set_password': True  # 标记需要设置密码
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"用户短信注册失败: {str(e)}")
            return Response({
                'status': 500,
                'msg': '注册失败，请稍后重试',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 400,
        'msg': '注册信息有误',
        'data': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """用户信息管理ViewSet"""
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """获取当前用户"""
        return self.request.user
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """获取用户详细信息"""
        user = request.user
        return Response({
            'status': 200,
            'msg': '获取成功',
            'data': UserDetailSerializer(user).data
        })
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """更新用户基本信息"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'msg': '更新成功',
                'data': serializer.data
            })
        
        return Response({
            'status': 400,
            'msg': '更新失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_user_profile(self, request):
        """更新用户详细资料"""
        user = request.user
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'msg': '资料更新成功',
                'data': serializer.data
            })
        
        return Response({
            'status': 400,
            'msg': '更新失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], throttle_classes=[ChangePwdThrottle])
    def change_password(self, request):
        """修改密码/首次设置密码"""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            
            # 判断是首次设置还是修改密码
            is_first_time = not user.has_usable_password()
            action = "设置" if is_first_time else "修改"
            
            # 使用序列化器的save方法
            tokens = serializer.save()
            
            logger.info(f"用户{action}密码: {user.phone}")
            
            return Response({
                'status': 200,
                'msg': f'密码{action}成功',
                'data': {'tokens': tokens}
            })
        
        return Response({
            'status': 400,
            'msg': '密码修改/设置失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='settings', url_name='user_settings')
    @method_decorator(cache_page(60 * 5))  # 缓存5分钟
    def user_settings(self, request):
        """获取用户设置"""
        user = request.user
        try:
            settings = user.settings
            return Response({
                'status': 200,
                'msg': '获取成功',
                'data': UserSettingSerializer(settings).data
            })
        except:
            return Response({
                'status': 404,
                'msg': '设置不存在',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_settings(self, request):
        """更新用户设置"""
        user = request.user
        try:
            settings = user.settings
        except:
            from .models import UserSetting
            settings = UserSetting.objects.create(user=user)
        
        serializer = UserSettingSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'msg': '设置更新成功',
                'data': serializer.data
            })
        
        return Response({
            'status': 400,
            'msg': '更新失败',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    用户登出API
    POST /api/auth/logout/
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        logger.info(f"用户登出: {request.user.phone}")
        
        return Response({
            'status': 200,
            'msg': '登出成功',
            'data': None
        })
    except Exception as e:
        return Response({
            'status': 400,
            'msg': '登出失败',
            'data': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
