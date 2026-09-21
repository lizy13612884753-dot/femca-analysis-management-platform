from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Max, Min, Avg

from .models import ProductHazardAnalysis
from .serializers import (
    ProductHazardAnalysisSerializer,
    ProductHazardAnalysisListSerializer
)
from auth_app.permissions import IsAdminOrReadOnly
from failure.models import FailureMode
from failure_analysis.models import FailureModeHazardAnalysis


class ProductHazardAnalysisViewSet(viewsets.ModelViewSet):
    """产品危害度分析管理视图集"""
    queryset = ProductHazardAnalysis.objects.select_related(
        'equipment_type', 'created_by'
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['equipment_type', 'overall_risk_level', 'is_active']
    search_fields = ['assessment_conclusion', 'recommendations']
    ordering_fields = ['analysis_date', 'avg_rpn', 'created_at']
    ordering = ['-analysis_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductHazardAnalysisListSerializer
        return ProductHazardAnalysisSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 只返回与活跃设备类型相关的分析结果
        queryset = queryset.filter(equipment_type__status='active')
        
        # 过滤出用户有权限访问的分析结果
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看自己创建的分析结果
            queryset = queryset.filter(created_by=user)
        
        return queryset

    @action(detail=False, methods=['get'])
    def by_equipment(self, request):
        """按设备类型获取分析结果"""
        equipment_type_id = request.query_params.get('equipment_type')
        if not equipment_type_id:
            return Response(
                {'error': '必须提供设备类型ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        analyses = self.get_queryset().filter(
            equipment_type_id=equipment_type_id
        ).order_by('-analysis_date')
        
        serializer = ProductHazardAnalysisListSerializer(analyses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest_analysis(self, request):
        """获取最新的分析结果"""
        equipment_type_id = request.query_params.get('equipment_type')
        
        queryset = self.get_queryset()
        if equipment_type_id:
            queryset = queryset.filter(equipment_type_id=equipment_type_id)
        
        latest_analysis = queryset.order_by('-analysis_date').first()
        
        if latest_analysis:
            serializer = ProductHazardAnalysisSerializer(latest_analysis)
            return Response(serializer.data)
        else:
            return Response(
                {'error': '未找到分析结果'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def overall_summary(self, request):
        """获取所有设备类型的汇总分析结果"""
        # 获取所有故障模式危害度分析
        all_hazard_analyses = FailureModeHazardAnalysis.objects.filter(is_active=True)
        
        # 汇总所有设备类型的故障模式（只计算活跃的故障模式）
        total_failure_modes = FailureMode.objects.filter(is_active=True).count()
        analyzed_failure_modes = all_hazard_analyses.count()
        
        # 计算统计数据
        if analyzed_failure_modes > 0:
            total_severity = sum(analysis.severity_value for analysis in all_hazard_analyses)
            total_occurrence = sum(analysis.occurrence_probability for analysis in all_hazard_analyses)
            total_detection = sum(analysis.detection_probability for analysis in all_hazard_analyses)
            total_rpn = sum(analysis.risk_priority_number for analysis in all_hazard_analyses)
            rpn_values = [analysis.risk_priority_number for analysis in all_hazard_analyses]
            
            avg_severity = total_severity / analyzed_failure_modes
            avg_occurrence = total_occurrence / analyzed_failure_modes
            avg_detection = total_detection / analyzed_failure_modes
            avg_rpn = total_rpn / analyzed_failure_modes
            max_rpn = max(rpn_values)
            min_rpn = min(rpn_values)
            
            # 风险等级计数
            risk_counts = {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
            for analysis in all_hazard_analyses:
                risk_counts[analysis.risk_level] += 1
        else:
            avg_severity = 0
            avg_occurrence = 0
            avg_detection = 0
            avg_rpn = 0
            max_rpn = 0
            min_rpn = 0
            risk_counts = {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
        
        # 确定整体风险等级
        if risk_counts['critical'] > 0:
            overall_risk_level = 'critical'
        elif risk_counts['high'] > (analyzed_failure_modes * 0.3):
            overall_risk_level = 'high'
        elif risk_counts['medium'] > (analyzed_failure_modes * 0.5):
            overall_risk_level = 'medium'
        else:
            overall_risk_level = 'low'
        
        # 构建汇总数据
        summary_data = {
            'id': None,
            'equipment_type': None,
            'equipment_type_name': '全部设备类型',
            'equipment_type_code': 'ALL',
            'analysis_date': None,
            'total_failure_modes': total_failure_modes,
            'analyzed_failure_modes': analyzed_failure_modes,
            'avg_severity': avg_severity,
            'avg_occurrence': avg_occurrence,
            'avg_detection': avg_detection,
            'avg_rpn': avg_rpn,
            'max_rpn': max_rpn,
            'min_rpn': min_rpn,
            'critical_count': risk_counts['critical'],
            'high_count': risk_counts['high'],
            'medium_count': risk_counts['medium'],
            'low_count': risk_counts['low'],
            'overall_risk_level': overall_risk_level,
            'risk_level_display': dict(ProductHazardAnalysis.RISK_LEVEL_CHOICES).get(overall_risk_level, overall_risk_level),
            'risk_level_distribution': {
                'critical': round((risk_counts['critical'] / analyzed_failure_modes) * 100, 2) if analyzed_failure_modes > 0 else 0,
                'high': round((risk_counts['high'] / analyzed_failure_modes) * 100, 2) if analyzed_failure_modes > 0 else 0,
                'medium': round((risk_counts['medium'] / analyzed_failure_modes) * 100, 2) if analyzed_failure_modes > 0 else 0,
                'low': round((risk_counts['low'] / analyzed_failure_modes) * 100, 2) if analyzed_failure_modes > 0 else 0
            },
            'assessment_conclusion': '整体风险水平评估完成，建议定期进行危害度分析。',
            'recommendations': '建议加强预防性维护，降低故障发生率。',
            'is_active': True,
            'created_by_name': '系统汇总',
            'created_at': None,
            'updated_at': None
        }
        
        return Response(summary_data)

    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        """重新计算分析结果"""
        analysis = self.get_object()
        
        try:
            analysis.update_analysis_data()
            serializer = ProductHazardAnalysisSerializer(analysis)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'重新计算失败: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取产品危害度分析统计数据"""
        # 计算各种统计数据
        total_analyses = self.get_queryset().count()
        total_equipment_types = self.get_queryset().values('equipment_type').distinct().count()
        
        # 计算平均值
        avg_stats = self.get_queryset().aggregate(
            avg_severity=Avg('avg_severity'),
            avg_occurrence=Avg('avg_occurrence'),
            avg_detection=Avg('avg_detection'),
            avg_rpn=Avg('avg_rpn')
        )
        
        # 计算最大值
        max_stats = self.get_queryset().aggregate(
            max_severity=Max('avg_severity'),
            max_occurrence=Max('avg_occurrence'),
            max_detection=Max('avg_detection'),
            max_rpn=Max('avg_rpn')
        )
        
        # 计算最小值
        min_stats = self.get_queryset().aggregate(
            min_severity=Min('avg_severity'),
            min_occurrence=Min('avg_occurrence'),
            min_detection=Min('avg_detection'),
            min_rpn=Min('avg_rpn')
        )
        
        # 整体风险等级分布
        risk_level_distribution = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        analyses = self.get_queryset()
        for analysis in analyses:
            risk_level_distribution[analysis.overall_risk_level] += 1
        
        # 构建统计数据响应
        statistics_data = {
            'total_analyses': total_analyses,
            'total_equipment_types': total_equipment_types,
            'average_values': {
                'severity': float(avg_stats['avg_severity']) if avg_stats['avg_severity'] else 0,
                'occurrence_probability': float(avg_stats['avg_occurrence']) if avg_stats['avg_occurrence'] else 0,
                'detection_probability': float(avg_stats['avg_detection']) if avg_stats['avg_detection'] else 0,
                'rpn': float(avg_stats['avg_rpn']) if avg_stats['avg_rpn'] else 0
            },
            'maximum_values': {
                'severity': float(max_stats['max_severity']) if max_stats['max_severity'] else 0,
                'occurrence_probability': float(max_stats['max_occurrence']) if max_stats['max_occurrence'] else 0,
                'detection_probability': float(max_stats['max_detection']) if max_stats['max_detection'] else 0,
                'rpn': float(max_stats['max_rpn']) if max_stats['max_rpn'] else 0
            },
            'minimum_values': {
                'severity': float(min_stats['min_severity']) if min_stats['min_severity'] else 0,
                'occurrence_probability': float(min_stats['min_occurrence']) if min_stats['min_occurrence'] else 0,
                'detection_probability': float(min_stats['min_detection']) if min_stats['min_detection'] else 0,
                'rpn': float(min_stats['min_rpn']) if min_stats['min_rpn'] else 0
            },
            'risk_level_distribution': risk_level_distribution
        }
        
        return Response(statistics_data)
