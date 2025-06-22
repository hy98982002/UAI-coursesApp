from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger('apps.utils')


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    统一API响应格式: { status, data, msg }
    """
    # 调用DRF默认的异常处理器
    response = exception_handler(exc, context)
    
    if response is not None:
        # 获取视图和请求信息
        view = context.get('view')
        request = context.get('request')
        
        # 记录异常日志
        if hasattr(view, '__class__'):
            view_name = view.__class__.__name__
        else:
            view_name = str(view)
            
        logger.error(f"API异常 - 视图: {view_name}, 异常: {str(exc)}, 状态码: {response.status_code}")
        
        # 自定义响应数据格式
        custom_response_data = {
            'status': response.status_code,
            'msg': get_error_message(response.data, response.status_code),
            'data': response.data if response.status_code < 500 else None
        }
        
        response.data = custom_response_data
    
    return response


def get_error_message(error_data, status_code):
    """
    根据错误数据和状态码生成友好的错误信息
    """
    if status_code == status.HTTP_400_BAD_REQUEST:
        if isinstance(error_data, dict):
            # 提取第一个字段的第一个错误信息
            for field, errors in error_data.items():
                if isinstance(errors, list) and len(errors) > 0:
                    return f"{field}: {errors[0]}"
                elif isinstance(errors, str):
                    return f"{field}: {errors}"
            return "请求参数有误"
        return "请求参数有误"
    
    elif status_code == status.HTTP_401_UNAUTHORIZED:
        return "认证失败，请重新登录"
    
    elif status_code == status.HTTP_403_FORBIDDEN:
        return "权限不足，无法访问"
    
    elif status_code == status.HTTP_404_NOT_FOUND:
        return "请求的资源不存在"
    
    elif status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        return "请求方法不被允许"
    
    elif status_code >= 500:
        return "服务器内部错误，请稍后重试"
    
    else:
        return "请求处理失败" 