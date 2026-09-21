from rest_framework import serializers
from .models import HazardAnalysisParameter, FailureModeHazardAnalysis


class HazardAnalysisParameterSerializer(serializers.ModelSerializer):
    """危害度参数配置序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = HazardAnalysisParameter
        fields = [
            'id', 'name', 'parameter_type', 'description', 'min_value',
            'max_value', 'default_value', 'unit', 'is_active',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']

    def create(self, validated_data):
        """创建危害度参数"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FailureModeHazardAnalysisSerializer(serializers.ModelSerializer):
    """故障模式危害度分析序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    failure_mode_code = serializers.CharField(source='failure_mode.code', read_only=True)
    severity_level_name = serializers.CharField(source='severity_level.name', read_only=True)
    severity_level_code = serializers.CharField(source='severity_level.level', read_only=True)
    
    # 风险等级显示名称
    risk_level_display = serializers.SerializerMethodField()

    class Meta:
        model = FailureModeHazardAnalysis
        fields = [
            'id', 'failure_mode', 'failure_mode_name', 'failure_mode_code',
            'severity_level', 'severity_level_name', 'severity_level_code',
            'severity_value', 'occurrence_probability', 'detection_probability',
            'risk_priority_number', 'risk_level', 'risk_level_display',
            'recommended_action', 'analysis_date', 'notes', 'is_active', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'created_by_name',
            'failure_mode_name', 'failure_mode_code',
            'severity_level_name', 'severity_level_code', 'risk_level_display',
            'risk_priority_number', 'risk_level'
        ]

    def create(self, validated_data):
        """创建故障模式危害度分析"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_risk_level_display(self, obj):
        """获取风险等级显示名称"""
        return dict(obj.RISK_LEVEL_CHOICES).get(obj.risk_level, obj.risk_level)


class FailureModeHazardAnalysisListSerializer(serializers.ModelSerializer):
    """故障模式危害度分析列表序列化器"""
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    failure_mode_code = serializers.CharField(source='failure_mode.code', read_only=True)
    severity_level_name = serializers.CharField(source='severity_level.name', read_only=True)
    risk_level_display = serializers.SerializerMethodField()

    class Meta:
        model = FailureModeHazardAnalysis
        fields = [
            'id', 'failure_mode', 'failure_mode_name', 'failure_mode_code',
            'severity_level_name', 'severity_value', 'occurrence_probability',
            'detection_probability', 'risk_priority_number', 'risk_level',
            'risk_level_display', 'recommended_action', 'analysis_date', 'is_active', 'created_at'
        ]
    
    def get_risk_level_display(self, obj):
        """获取风险等级显示名称"""
        return dict(obj.RISK_LEVEL_CHOICES).get(obj.risk_level, obj.risk_level)
