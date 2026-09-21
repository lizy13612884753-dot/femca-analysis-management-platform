from rest_framework import serializers
from .models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    """用户设置序列化器"""
    
    class Meta:
        model = UserSettings
        fields = [
            'id',
            'theme',
            'language',
            'page_size',
            'auto_save',
            'email_enabled',
            'system_enabled',
            'failure_alert',
            'analysis_complete',
            'report_ready',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
