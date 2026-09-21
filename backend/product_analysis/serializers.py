from rest_framework import serializers
from .models import ProductHazardAnalysis


class ProductHazardAnalysisSerializer(serializers.ModelSerializer):
    """产品危害度分析序列化器"""
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)
    equipment_type_code = serializers.CharField(source='equipment_type.code', read_only=True)
    
    # 风险等级显示名称
    risk_level_display = serializers.SerializerMethodField()
    
    # 风险等级分布百分比
    risk_level_distribution = serializers.SerializerMethodField()

    class Meta:
        model = ProductHazardAnalysis
        fields = [
            'id', 'equipment_type', 'equipment_type_name', 'equipment_type_code',
            'analysis_date', 'total_failure_modes', 'analyzed_failure_modes',
            'avg_severity', 'avg_occurrence', 'avg_detection', 'avg_rpn',
            'max_rpn', 'min_rpn', 'critical_count', 'high_count',
            'medium_count', 'low_count', 'overall_risk_level', 'risk_level_display',
            'risk_level_distribution', 'assessment_conclusion', 'recommendations',
            'is_active', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'created_by_name',
            'equipment_type_name', 'equipment_type_code', 'risk_level_display',
            'risk_level_distribution'
        ]

    def create(self, validated_data):
        """创建产品危害度分析"""
        validated_data['created_by'] = self.context['request'].user
        analysis = super().create(validated_data)
        
        # 更新分析数据
        analysis.update_analysis_data()
        return analysis
    
    def update(self, instance, validated_data):
        """更新产品危害度分析"""
        analysis = super().update(instance, validated_data)
        
        # 更新分析数据
        analysis.update_analysis_data()
        return analysis
    
    def get_risk_level_display(self, obj):
        """获取风险等级显示名称"""
        return dict(obj.RISK_LEVEL_CHOICES).get(obj.overall_risk_level, obj.overall_risk_level)
    
    def get_risk_level_distribution(self, obj):
        """获取风险等级分布百分比"""
        if obj.analyzed_failure_modes == 0:
            return {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
        
        return {
            'critical': round((obj.critical_count / obj.analyzed_failure_modes) * 100, 2),
            'high': round((obj.high_count / obj.analyzed_failure_modes) * 100, 2),
            'medium': round((obj.medium_count / obj.analyzed_failure_modes) * 100, 2),
            'low': round((obj.low_count / obj.analyzed_failure_modes) * 100, 2)
        }


class ProductHazardAnalysisListSerializer(serializers.ModelSerializer):
    """产品危害度分析列表序列化器"""
    equipment_type_name = serializers.CharField(source='equipment_type.name', read_only=True)
    equipment_type_code = serializers.CharField(source='equipment_type.code', read_only=True)
    risk_level_display = serializers.SerializerMethodField()
    
    # 风险等级分布概览
    risk_level_overview = serializers.SerializerMethodField()

    class Meta:
        model = ProductHazardAnalysis
        fields = [
            'id', 'equipment_type', 'equipment_type_name', 'equipment_type_code',
            'analysis_date', 'total_failure_modes', 'analyzed_failure_modes',
            'avg_rpn', 'max_rpn', 'overall_risk_level', 'risk_level_display',
            'risk_level_overview', 'is_active', 'created_at'
        ]
    
    def get_risk_level_display(self, obj):
        """获取风险等级显示名称"""
        return dict(obj.RISK_LEVEL_CHOICES).get(obj.overall_risk_level, obj.overall_risk_level)
    
    def get_risk_level_overview(self, obj):
        """获取风险等级分布概览"""
        return {
            'critical': obj.critical_count,
            'high': obj.high_count,
            'medium': obj.medium_count,
            'low': obj.low_count
        }
