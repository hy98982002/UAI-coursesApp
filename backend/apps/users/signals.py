from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, UserSetting


@receiver(post_save, sender=User)
def create_user_profile_and_settings(sender, instance, created, **kwargs):
    """
    用户创建后自动创建相关的Profile和Setting记录
    优化：使用get_or_create避免并发重复创建
    """
    if created:
        # 使用get_or_create确保并发安全
        UserProfile.objects.get_or_create(user=instance)
        UserSetting.objects.get_or_create(user=instance) 