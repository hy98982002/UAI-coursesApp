"""
用户模块工具函数
"""
import random
import string
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger('apps.users')


class SmsCodeManager:
    """短信验证码管理器"""
    
    # 验证码配置
    CODE_LENGTH = 6
    CODE_EXPIRE_MINUTES = 5
    MAX_SEND_COUNT = 5  # 每小时最大发送次数
    
    @classmethod
    def generate_code(cls) -> str:
        """生成6位数字验证码"""
        return ''.join(random.choices(string.digits, k=cls.CODE_LENGTH))
    
    @classmethod
    def get_cache_key(cls, phone: str, code_type: str = 'default') -> str:
        """获取缓存键名"""
        return f"sms_code:{code_type}:{phone}"
    
    @classmethod
    def get_send_count_key(cls, phone: str) -> str:
        """获取发送次数缓存键名"""
        return f"sms_send_count:{phone}"
    
    @classmethod
    def store_code(cls, phone: str, code: str, code_type: str = 'default') -> bool:
        """
        存储验证码到缓存
        :param phone: 手机号
        :param code: 验证码
        :param code_type: 验证码类型 (register, login, reset_password等)
        :return: 是否成功
        """
        try:
            cache_key = cls.get_cache_key(phone, code_type)
            cache_data = {
                'code': code,
                'phone': phone,
                'created_at': datetime.now().isoformat(),
                'code_type': code_type
            }
            
            # 存储验证码，5分钟过期
            cache.set(cache_key, cache_data, timeout=cls.CODE_EXPIRE_MINUTES * 60)
            
            logger.info(f"验证码已存储: {phone} - {code_type}")
            return True
        except Exception as e:
            logger.error(f"存储验证码失败: {phone} - {str(e)}")
            return False
    
    @classmethod
    def verify_code(cls, phone: str, code: str, code_type: str = 'default') -> dict:
        """
        验证验证码
        :param phone: 手机号
        :param code: 用户输入的验证码
        :param code_type: 验证码类型
        :return: 验证结果字典
        """
        cache_key = cls.get_cache_key(phone, code_type)
        
        try:
            cache_data = cache.get(cache_key)
            
            if not cache_data:
                logger.warning(f"验证码不存在或已过期: {phone} - {code_type}")
                return {
                    'valid': False,
                    'message': '验证码不存在或已过期',
                    'error_code': 'CODE_EXPIRED'
                }
            
            stored_code = cache_data.get('code')
            if stored_code != code:
                logger.warning(f"验证码错误: {phone} - 输入:{code}, 正确:{stored_code}")
                return {
                    'valid': False,
                    'message': '验证码错误',
                    'error_code': 'CODE_INVALID'
                }
            
            # 验证成功，删除验证码（一次性使用）
            cache.delete(cache_key)
            logger.info(f"验证码验证成功: {phone} - {code_type}")
            
            return {
                'valid': True,
                'message': '验证码验证成功',
                'data': cache_data
            }
            
        except Exception as e:
            logger.error(f"验证码验证异常: {phone} - {str(e)}")
            return {
                'valid': False,
                'message': '验证码验证失败',
                'error_code': 'VERIFY_ERROR'
            }
    
    @classmethod
    def can_send_code(cls, phone: str) -> dict:
        """
        检查是否可以发送验证码
        :param phone: 手机号
        :return: 检查结果
        """
        send_count_key = cls.get_send_count_key(phone)
        current_count = cache.get(send_count_key, 0)
        
        if current_count >= cls.MAX_SEND_COUNT:
            return {
                'can_send': False,
                'message': f'每小时最多发送{cls.MAX_SEND_COUNT}次验证码，请稍后再试',
                'error_code': 'SEND_LIMIT_EXCEEDED'
            }
        
        return {
            'can_send': True,
            'remaining_count': cls.MAX_SEND_COUNT - current_count
        }
    
    @classmethod
    def record_send(cls, phone: str) -> bool:
        """
        记录发送次数
        :param phone: 手机号
        :return: 是否成功
        """
        try:
            send_count_key = cls.get_send_count_key(phone)
            current_count = cache.get(send_count_key, 0)
            
            # 记录发送次数，1小时过期
            cache.set(send_count_key, current_count + 1, timeout=3600)
            logger.info(f"记录验证码发送次数: {phone} - {current_count + 1}")
            return True
        except Exception as e:
            logger.error(f"记录发送次数失败: {phone} - {str(e)}")
            return False
    
    @classmethod
    def get_development_code(cls) -> str:
        """
        开发环境获取固定验证码
        """
        if settings.DEBUG:
            return '123456'
        return None


def format_phone_number(phone: str) -> str:
    """
    格式化手机号（脱敏显示）
    """
    if len(phone) == 11:
        return f"{phone[:3]}****{phone[-4:]}"
    return phone[:3] + "*" * (len(phone) - 6) + phone[-3:]


def is_valid_phone(phone: str) -> bool:
    """
    验证手机号格式
    """
    import re
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone)) 