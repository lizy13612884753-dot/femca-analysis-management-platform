from rest_framework import serializers
from .models import DetectionMethod, DetectionRating, FailureModeDetection
from failure.models import FailureMode


class DetectionMethodSerializer(serializers.ModelSerializer):
    """检测方法序列化器"""
    method_type_display = serializers.CharField(source='get_method_type_display_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    equipment_types_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = DetectionMethod
        fields = ['id', 'name', 'code', 'description', 'method_type', 'method_type_display',
                 'equipment_types', 'equipment_types_detail', 'cost', 'time_required', 
                 'accuracy', 'is_active', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name', 'equipment_types_detail']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_equipment_types_detail(self, obj):
        equipment_types = obj.equipment_types.all()
        return [{'id': eq_type.id, 'name': eq_type.name, 'code': eq_type.code} 
                for eq_type in equipment_types]


class DetectionRatingSerializer(serializers.ModelSerializer):
    """检测评级序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DetectionRating
        fields = ['id', 'rating', 'name', 'description', 'rpn_score', 'detection_time',
                 'is_active', 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class FailureModeDetectionSerializer(serializers.ModelSerializer):
    """故障模式检测关联序列化器"""
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    detection_method_name = serializers.CharField(source='detection_method.name', read_only=True)
    detection_method_code = serializers.CharField(source='detection_method.code', read_only=True)
    detection_rating_display = serializers.CharField(source='detection_rating.__str__', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = FailureModeDetection
        fields = ['id', 'failure_mode', 'failure_mode_name', 'detection_method', 
                 'detection_method_name', 'detection_method_code', 'detection_rating', 
                 'detection_rating_display', 'notes', 'is_active', 'created_by_name', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'failure_mode_name', 
                           'detection_method_name', 'detection_method_code', 
                           'detection_rating_display', 'created_by_name']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class DetectionMethodListSerializer(serializers.ModelSerializer):
    """检测方法列表序列化器"""
    method_type_display = serializers.CharField(source='get_method_type_display_name', read_only=True)
    equipment_type_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DetectionMethod
        fields = ['id', 'name', 'code', 'method_type', 'method_type_display',
                 'cost', 'time_required', 'accuracy', 'is_active', 'equipment_type_count',
                 'created_at']
    
    def get_equipment_type_count(self, obj):
        return obj.equipment_types.count()


class DetectionRatingListSerializer(serializers.ModelSerializer):
    """检测评级列表序列化器"""
    
    class Meta:
        model = DetectionRating
        fields = ['id', 'rating', 'name', 'rpn_score', 'detection_time', 'is_active', 'created_at']


class FailureModeDetectionListSerializer(serializers.ModelSerializer):
    """故障模式检测关联列表序列化器"""
    failure_mode_name = serializers.CharField(source='failure_mode.name', read_only=True)
    detection_method_name = serializers.CharField(source='detection_method.name', read_only=True)
    detection_method_code = serializers.CharField(source='detection_method.code', read_only=True)
    detection_rating_display = serializers.CharField(source='detection_rating.__str__', read_only=True)
    
    class Meta:
        model = FailureModeDetection
        fields = ['id', 'failure_mode', 'failure_mode_name', 'detection_method', 
                 'detection_method_name', 'detection_method_code', 'detection_rating', 
                 'detection_rating_display', 'is_active', 'created_at']


class DetectionMethodSearchSerializer(serializers.Serializer):
    """检测方法搜索序列化器"""
    name = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    method_type = serializers.ChoiceField(choices=DetectionMethod.METHOD_TYPE_CHOICES, required=False)
    equipment_type = serializers.PrimaryKeyRelatedField(
        queryset=DetectionMethod._meta.get_field('equipment_types').remote_field.model.objects.all(),
        required=False
    )
    is_active = serializers.BooleanField(required=False)


class FailureModeDetectionSearchSerializer(serializers.Serializer):
    """故障模式检测关联搜索序列化器"""
    failure_mode = serializers.PrimaryKeyRelatedField(
        queryset=FailureMode.objects.all(),
        required=False
    )
    detection_method = serializers.PrimaryKeyRelatedField(
        queryset=DetectionMethod.objects.all(),
        required=False
    )
    detection_rating = serializers.PrimaryKeyRelatedField(
        queryset=DetectionRating.objects.all(),
        required=False
    )
    is_active = serializers.BooleanField(required=False)