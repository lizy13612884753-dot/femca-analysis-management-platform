from rest_framework import serializers
from .models import EquipmentType, EquipmentInstance


class EquipmentTypeSerializer(serializers.ModelSerializer):
    """设备类型序列化器"""
    status_display = serializers.CharField(source='get_status_display_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'code', 'description', 'category', 'manufacturer', 'model',
                 'specifications', 'status', 'status_display', 'created_by_name', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name']
        extra_kwargs = {
            'created_at': {'format': '%Y-%m-%d %H:%M:%S'},
            'updated_at': {'format': '%Y-%m-%d %H:%M:%S'}
        }
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EquipmentInstanceSerializer(serializers.ModelSerializer):
    """设备实例序列化器"""
    status_display = serializers.CharField(source='get_status_display_name', read_only=True)
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)
    equipment_type_code = serializers.CharField(source='equipment_type.code', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = EquipmentInstance
        fields = ['id', 'equipment_type', 'equipment_type_name', 'equipment_type_code',
                 'serial_number', 'name', 'location', 'install_date', 'warranty_expire_date',
                 'status', 'status_display', 'custom_specifications', 'function_description', 'notes',
                 'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by_name',
                           'equipment_type_name', 'equipment_type_code']
        extra_kwargs = {
            'created_at': {'format': '%Y-%m-%d %H:%M:%S'},
            'updated_at': {'format': '%Y-%m-%d %H:%M:%S'}
        }
    
    def validate_install_date(self, value):
        """验证安装日期字段"""
        if isinstance(value, list) and len(value) > 0:
            # 如果是数组，取第一个元素
            return value[0]
        return value

    def validate_warranty_expire_date(self, value):
        """验证保修到期日期字段"""
        if isinstance(value, list) and len(value) > 0:
            # 如果是数组，取第一个元素
            return value[0]
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EquipmentTypeListSerializer(serializers.ModelSerializer):
    """设备类型列表序列化器"""
    status_display = serializers.CharField(source='get_status_display_name', read_only=True)
    instance_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'code', 'category', 'manufacturer', 'model',
                 'status', 'status_display', 'instance_count', 'created_by_name', 'created_at']
        extra_kwargs = {
            'created_at': {'format': '%Y-%m-%d %H:%M:%S'}
        }
    
    def get_instance_count(self, obj):
        return obj.instances.count()


# 创建一个新的简单序列化器，确保包含function_description字段
class SimpleEquipmentInstanceSerializer(serializers.ModelSerializer):
    """简化的设备实例序列化器"""
    status_display = serializers.CharField(source='get_status_display_name', read_only=True)
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)
    equipment_type_code = serializers.CharField(source='equipment_type.code', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = EquipmentInstance
        fields = ['id', 'equipment_type', 'equipment_type_name', 'equipment_type_code',
                 'serial_number', 'name', 'location', 'status', 'status_display',
                 'function_description', 'created_by_name', 'created_at']
        extra_kwargs = {
            'created_at': {'format': '%Y-%m-%d %H:%M:%S'}
        }

class EquipmentInstanceListSerializer(SimpleEquipmentInstanceSerializer):
    """设备实例列表序列化器"""
    display_id = serializers.SerializerMethodField()
    
    class Meta(SimpleEquipmentInstanceSerializer.Meta):
        fields = SimpleEquipmentInstanceSerializer.Meta.fields + ['display_id']
    
    def get_display_id(self, obj):
        """计算连续显示ID"""
        # 获取当前对象在查询集中的索引
        try:
            # 从上下文中获取查询集和分页信息
            queryset = self.context.get('queryset', [])
            page = self.context.get('page', None)
            request = self.context.get('request', None)
            
            if page and request:
                # 有分页的情况
                page_number = page.number
                page_size = page.paginator.per_page
                # 获取当前对象在当前页中的索引
                if hasattr(obj, 'display_id'):
                    return obj.display_id
                elif obj in page:
                    index = list(page).index(obj)
                    return (page_number - 1) * page_size + index + 1
            else:
                # 没有分页的情况
                if hasattr(obj, 'display_id'):
                    return obj.display_id
                elif obj in queryset:
                    return list(queryset).index(obj) + 1
            
            # 如果以上方法都失败，返回数据库ID
            return obj.id
        except:
            # 出现异常时返回数据库ID
            return obj.id


class EquipmentTypeSearchSerializer(serializers.Serializer):
    """设备类型搜索序列化器"""
    name = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    manufacturer = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=EquipmentType.STATUS_CHOICES, required=False)


class EquipmentStatisticsSerializer(serializers.Serializer):
    """设备统计序列化器"""
    total_types = serializers.IntegerField()
    total_instances = serializers.IntegerField()
    active_types = serializers.IntegerField()
    operational_instances = serializers.IntegerField()
    maintenance_instances = serializers.IntegerField()
    fault_instances = serializers.IntegerField()
    types_by_category = serializers.DictField()
    instances_by_status = serializers.DictField()