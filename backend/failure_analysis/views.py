from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Max, Min

from .models import HazardAnalysisParameter, FailureModeHazardAnalysis
from .serializers import (
    HazardAnalysisParameterSerializer,
    FailureModeHazardAnalysisSerializer,
    FailureModeHazardAnalysisListSerializer
)
from auth_app.permissions import IsAdminOrReadOnly


class HazardAnalysisParameterViewSet(viewsets.ModelViewSet):
    """危害度参数配置管理视图集"""
    queryset = HazardAnalysisParameter.objects.select_related('created_by').all()
    serializer_class = HazardAnalysisParameterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parameter_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'parameter_type', 'created_at']
    ordering = ['parameter_type', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 过滤出用户有权限访问的参数
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看启用的参数
            queryset = queryset.filter(is_active=True)
        
        return queryset

    @action(detail=False, methods=['get'])
    def active_parameters(self, request):
        """获取所有活跃的参数"""
        parameters = HazardAnalysisParameter.objects.filter(is_active=True)
        serializer = HazardAnalysisParameterSerializer(parameters, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按参数类型获取参数"""
        parameter_type = request.query_params.get('type')
        if not parameter_type:
            return Response(
                {'error': '必须提供参数类型'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        parameters = HazardAnalysisParameter.objects.filter(
            parameter_type=parameter_type, 
            is_active=True
        )
        serializer = HazardAnalysisParameterSerializer(parameters, many=True)
        return Response(serializer.data)


class FailureModeHazardAnalysisViewSet(viewsets.ModelViewSet):
    """故障模式危害度分析管理视图集"""
    queryset = FailureModeHazardAnalysis.objects.select_related(
        'failure_mode', 'severity_level', 'created_by'
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['failure_mode', 'severity_level', 'risk_level', 'is_active']
    search_fields = ['notes']
    ordering_fields = ['risk_priority_number', 'severity_value', 'occurrence_probability', 'created_at']
    ordering = ['-risk_priority_number']

    def get_serializer_class(self):
        if self.action == 'list':
            return FailureModeHazardAnalysisListSerializer
        return FailureModeHazardAnalysisSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 产品分析页面需要显示所有故障模式数据，不过滤用户权限
        # 这样可以确保所有用户都能看到完整的风险排名
        
        return queryset

    def create(self, request, *args, **kwargs):
        """创建故障模式危害度分析"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"验证失败: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取危害度分析统计数据"""
        # 计算各种统计数据
        total_analyses = self.get_queryset().count()
        
        # 计算平均值
        avg_stats = self.get_queryset().aggregate(
            avg_severity=Avg('severity_value'),
            avg_occurrence=Avg('occurrence_probability'),
            avg_detection=Avg('detection_probability'),
            avg_rpn=Avg('risk_priority_number')
        )
        
        # 计算最大值
        max_stats = self.get_queryset().aggregate(
            max_severity=Max('severity_value'),
            max_occurrence=Max('occurrence_probability'),
            max_detection=Max('detection_probability'),
            max_rpn=Max('risk_priority_number')
        )
        
        # 计算最小值
        min_stats = self.get_queryset().aggregate(
            min_severity=Min('severity_value'),
            min_occurrence=Min('occurrence_probability'),
            min_detection=Min('detection_probability'),
            min_rpn=Min('risk_priority_number')
        )
        
        # 风险等级分布
        risk_level_distribution = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        analyses = self.get_queryset()
        for analysis in analyses:
            risk_level_distribution[analysis.risk_level] += 1
        
        # 构建统计数据响应
        statistics_data = {
            'total_analyses': total_analyses,
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

    @action(detail=False, methods=['get'])
    def top_risk(self, request):
        """获取风险最高的故障模式"""
        limit = int(request.query_params.get('limit', 10))
        top_risk_analyses = self.get_queryset().order_by('-risk_priority_number')[:limit]
        serializer = FailureModeHazardAnalysisListSerializer(top_risk_analyses, many=True)
        return Response(serializer.data)
