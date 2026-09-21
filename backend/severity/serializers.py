from rest_framework import serializers
from .models import SeverityLevel, SeverityIndicator, SeverityAssessment


class SeverityLevelSerializer(serializers.ModelSerializer):
    """严酷度等级序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = SeverityLevel
        fields = [
            'id', 'level', 'name', 'description', 'criteria', 'score',
            'is_active', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']

    def create(self, validated_data):
        """创建严酷度等级"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class SeverityIndicatorSerializer(serializers.ModelSerializer):
    """严酷度指标序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = SeverityIndicator
        fields = [
            'id', 'name', 'code', 'description', 'weight',
            'is_active', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']

    def create(self, validated_data):
        """创建严酷度指标"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class SeverityAssessmentSerializer(serializers.ModelSerializer):
    """严酷度评定序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    failure_mode_code = serializers.CharField(source='failure_mode.code', read_only=True)
    severity_level_name = serializers.CharField(source='severity_level.name', read_only=True)
    severity_level_code = serializers.CharField(source='severity_level.level', read_only=True)

    class Meta:
        model = SeverityAssessment
        fields = [
            'id', 'failure_mode', 'failure_mode_name', 'failure_mode_code', 'severity_level',
            'severity_level_name', 'severity_level_code', 'severity_value',
            'occurrence_value', 'detection_value', 'rpn_value', 'score', 
            'project_instance_name', 'evaluation', 'evidence', 'is_active', 'created_by_name', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'created_by_name',
            'failure_mode_name', 'severity_level_name', 'severity_level_code'
        ]

    def create(self, validated_data):
        """创建严酷度评定"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
