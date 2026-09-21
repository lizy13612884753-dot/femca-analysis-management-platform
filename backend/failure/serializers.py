from rest_framework import serializers
from .models import FailureMode, FailureCause, FailureEffect


class FailureCauseSerializer(serializers.ModelSerializer):
    """故障原因序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = FailureCause
        fields = [
            'id', 'name', 'description', 'failure_mode',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']

    def create(self, validated_data):
        """创建故障原因"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FailureEffectSerializer(serializers.ModelSerializer):
    """故障影响序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = FailureEffect
        fields = [
            'id', 'name', 'description', 'failure_mode', 'severity',
            'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']

    def create(self, validated_data):
        """创建故障影响"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FailureModeSerializer(serializers.ModelSerializer):
    """故障模式序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    failure_causes = FailureCauseSerializer(many=True, read_only=True)
    failure_effects = FailureEffectSerializer(many=True, read_only=True)

    class Meta:
        model = FailureMode
        fields = [
            'id', 'name', 'code', 'description', 'equipment_type',
            'function_name', 'function_status', 'failure_effect', 'severity',
            'severity_score', 'occurrence_rate', 'frequency', 'causes',
            'detection_methods', 'failure_causes', 'failure_effects', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']

    def create(self, validated_data):
        """创建故障模式"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FailureModeListSerializer(serializers.ModelSerializer):
    """故障模式列表序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)

    class Meta:
        model = FailureMode
        fields = [
            'id', 'name', 'code', 'equipment_type', 'equipment_type_name',
            'function_name', 'severity', 'causes', 'failure_effect',
            'created_by_name', 'created_at'
        ]
