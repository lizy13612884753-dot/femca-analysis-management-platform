from rest_framework import serializers
from django.contrib.auth import get_user_model
from equipment.models import EquipmentType
from failure.models import FailureMode
from .models import CompensationMeasure, EffectivenessEvaluation, FailureModeCompensation

User = get_user_model()


class CompensationMeasureSerializer(serializers.ModelSerializer):
    """补偿措施序列化器"""
    measure_type_display = serializers.CharField(source='get_measure_type_display_name', read_only=True)
    complexity_display = serializers.CharField(source='get_complexity_display_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    equipment_types_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = CompensationMeasure
        fields = ['id', 'name', 'code', 'description', 'measure_type', 'measure_type_display',
                 'equipment_types', 'equipment_types_detail', 'cost', 'time_required', 
                 'effectiveness', 'implementation_complexity', 'complexity_display',
                 'is_active', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name', 'equipment_types_detail']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_equipment_types_detail(self, obj):
        equipment_types = obj.equipment_types.all()
        return [{'id': eq_type.id, 'name': eq_type.name, 'code': eq_type.code} 
                for eq_type in equipment_types]


class EffectivenessEvaluationSerializer(serializers.ModelSerializer):
    """有效性评估序列化器"""
    compensation_measure_name = serializers.CharField(source='compensation_measure.name', read_only=True)
    compensation_measure_code = serializers.CharField(source='compensation_measure.code', read_only=True)
    evaluator_name = serializers.CharField(source='evaluator.username', read_only=True)
    
    class Meta:
        model = EffectivenessEvaluation
        fields = ['id', 'compensation_measure', 'compensation_measure_name', 
                 'compensation_measure_code', 'evaluation_date', 'evaluator', 
                 'evaluator_name', 'actual_effectiveness', 'notes', 'is_active', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'compensation_measure_name', 
                           'compensation_measure_code', 'evaluator_name']


class FailureModeCompensationSerializer(serializers.ModelSerializer):
    """故障模式补偿关联序列化器"""
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    compensation_measure_name = serializers.CharField(source='compensation_measure.name', read_only=True)
    compensation_measure_code = serializers.CharField(source='compensation_measure.code', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = FailureModeCompensation
        fields = ['id', 'failure_mode', 'failure_mode_name', 'compensation_measure', 
                 'compensation_measure_name', 'compensation_measure_code', 
                 'effectiveness_rating', 'rating_display', 'notes', 'is_active', 
                 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'failure_mode_name', 
                           'compensation_measure_name', 'compensation_measure_code', 
                           'rating_display', 'created_by_name']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CompensationMeasureListSerializer(serializers.ModelSerializer):
    """补偿措施列表序列化器"""
    measure_type_display = serializers.CharField(source='get_measure_type_display_name', read_only=True)
    complexity_display = serializers.CharField(source='get_complexity_display_name', read_only=True)
    equipment_type_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CompensationMeasure
        fields = ['id', 'name', 'code', 'measure_type', 'measure_type_display',
                 'effectiveness', 'implementation_complexity', 'complexity_display',
                 'cost', 'time_required', 'is_active', 'equipment_type_count', 'created_at']
    
    def get_equipment_type_count(self, obj):
        return obj.equipment_types.count()


class EffectivenessEvaluationListSerializer(serializers.ModelSerializer):
    """有效性评估列表序列化器"""
    compensation_measure_name = serializers.CharField(source='compensation_measure.name', read_only=True)
    evaluator_name = serializers.CharField(source='evaluator.username', read_only=True)
    
    class Meta:
        model = EffectivenessEvaluation
        fields = ['id', 'compensation_measure', 'compensation_measure_name', 
                 'evaluation_date', 'evaluator', 'evaluator_name', 
                 'actual_effectiveness', 'is_active', 'created_at']


class FailureModeCompensationListSerializer(serializers.ModelSerializer):
    """故障模式补偿关联列表序列化器"""
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    compensation_measure_name = serializers.CharField(source='compensation_measure.name', read_only=True)
    compensation_measure_code = serializers.CharField(source='compensation_measure.code', read_only=True)
    rating_display = serializers.CharField(source='get_rating_display_name', read_only=True)
    
    class Meta:
        model = FailureModeCompensation
        fields = ['id', 'failure_mode', 'failure_mode_name', 'compensation_measure', 
                 'compensation_measure_name', 'compensation_measure_code', 
                 'effectiveness_rating', 'rating_display', 'is_active', 'created_at']


class CompensationMeasureSearchSerializer(serializers.Serializer):
    """补偿措施搜索序列化器"""
    name = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    measure_type = serializers.ChoiceField(choices=CompensationMeasure.MEASURE_TYPE_CHOICES, required=False)
    equipment_type = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentType.objects.all(),
        required=False
    )
    implementation_complexity = serializers.ChoiceField(
        choices=CompensationMeasure.COMPLEXITY_CHOICES, 
        required=False
    )
    is_active = serializers.BooleanField(required=False)


class EffectivenessEvaluationSearchSerializer(serializers.Serializer):
    """有效性评估搜索序列化器"""
    compensation_measure = serializers.PrimaryKeyRelatedField(
        queryset=CompensationMeasure.objects.all(),
        required=False
    )
    evaluator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    is_active = serializers.BooleanField(required=False)


class FailureModeCompensationSearchSerializer(serializers.Serializer):
    """故障模式补偿关联搜索序列化器"""
    failure_mode = serializers.PrimaryKeyRelatedField(
        queryset=FailureMode.objects.all(),
        required=False
    )
    compensation_measure = serializers.PrimaryKeyRelatedField(
        queryset=CompensationMeasure.objects.all(),
        required=False
    )
    effectiveness_rating = serializers.ChoiceField(
        choices=FailureModeCompensation.RATING_CHOICES, 
        required=False
    )
    is_active = serializers.BooleanField(required=False)