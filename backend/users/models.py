from django.db import models
from django.conf import settings


class UserSettings(models.Model):
    """用户设置模型"""
    
    THEME_CHOICES = [
        ('light', '浅色'),
        ('dark', '深色'),
        ('auto', '跟随系统'),
    ]
    
    LANGUAGE_CHOICES = [
        ('zh-CN', '简体中文'),
        ('en-US', 'English'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name='用户'
    )
    
    # 偏好设置
    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='light',
        verbose_name='主题'
    )
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='zh-CN',
        verbose_name='语言'
    )
    page_size = models.IntegerField(default=20, verbose_name='每页显示条数')
    auto_save = models.BooleanField(default=True, verbose_name='自动保存')
    
    # 通知设置
    email_enabled = models.BooleanField(default=True, verbose_name='邮件通知')
    system_enabled = models.BooleanField(default=True, verbose_name='系统通知')
    failure_alert = models.BooleanField(default=True, verbose_name='故障提醒')
    analysis_complete = models.BooleanField(default=True, verbose_name='分析完成提醒')
    report_ready = models.BooleanField(default=True, verbose_name='报告生成提醒')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user_settings'
        verbose_name = '用户设置'
        verbose_name_plural = '用户设置'

    def __str__(self):
        return f"{self.user.username}的设置"
