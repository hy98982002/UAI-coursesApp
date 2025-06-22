from rest_framework.throttling import UserRateThrottle


class ChangePwdThrottle(UserRateThrottle):
    """密码修改专用速率限制"""
    scope = "change_pwd" 