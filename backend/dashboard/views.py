from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Max, Min, Sum
from django.utils import timezone
from datetime import datetime, timedelta

from equipment.models import EquipmentType, EquipmentInstance
from failure.models import FailureMode, FailureCause, FailureEffect
from severity.models import SeverityLevel, SeverityAssessment
from detection.models import DetectionMethod, DetectionRating, FailureModeDetection
from compensation.models import CompensationMeasure, EffectivenessEvaluation, FailureModeCompensation
from failure_analysis.models import FailureModeHazardAnalysis
from product_analysis.models import ProductHazardAnalysis


class DashboardViewSet(viewsets.GenericViewSet):
    """数据统计与可视化视图集"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """获取查询集"""
        return None
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """首页数据概览"""
        user = request.user
        
        # 计算设备相关统计（与设备管理页面保持一致）
        equipment_stats = {
            'total_equipment_types': EquipmentType.objects.select_related('created_by').count(),
            'total_equipment_instances': EquipmentInstance.objects.select_related('equipment_type', 'created_by').count(),
        }
        
        # 计算设备状态分布
        status_distribution = EquipmentInstance.objects.values('status').annotate(count=Count('id'))
        
        # 定义设备状态的中文名称
        status_names = {
            'operational': '运行中',
            'maintenance': '维护中',
            'fault': '故障',
            'offline': '离线',
            'decommissioned': '已退役'
        }
        
        # 构建完整的设备状态分布数据
        full_status_distribution = {
            'operational': 0,
            'maintenance': 0,
            'fault': 0,
            'offline': 0,
            'decommissioned': 0
        }
        
        for item in status_distribution:
            full_status_distribution[item['status']] = item['count']
        
        # 转换为前端需要的格式
        equipment_stats['status_distribution'] = [
            {'value': full_status_distribution[key], 'name': status_names[key]}
            for key in full_status_distribution.keys()
        ]
        
        # 计算故障相关统计
        failure_stats = {
            'total_failure_modes': FailureMode.objects.count(),
            'total_failure_causes': FailureCause.objects.count(),
            'total_failure_effects': FailureEffect.objects.count(),
        }
        
        # 计算故障模式分布
        mode_distribution = FailureMode.objects.values('name').annotate(count=Count('id'))
        
        # 转换为前端需要的格式
        failure_stats['mode_distribution'] = [
            {'value': item['count'], 'name': item['name']}
            for item in mode_distribution
        ]
        
        # 计算危害度分析统计
        hazard_analysis_stats = {
            'analyzed_failure_modes': FailureModeHazardAnalysis.objects.filter(is_active=True).count(),
            'total_product_analyses': ProductHazardAnalysis.objects.count(),
        }
        
        # 获取最近活动
        recent_activities = []
        
        # 1. 设备类型最近创建记录
        equipment_types = EquipmentType.objects.select_related('created_by').order_by('-created_at')[:5]
        for et in equipment_types:
            recent_activities.append({
                'id': f'equipment_type_{et.id}',
                'description': f'新增设备类型：{et.name}',
                'timestamp': timezone.localtime(et.created_at).strftime('%Y-%m-%d %H:%M'),
                'type': 'primary'
            })
        
        # 2. 设备实例最近创建记录
        equipment_instances = EquipmentInstance.objects.select_related('equipment_type', 'created_by').order_by('-created_at')[:5]
        for ei in equipment_instances:
            recent_activities.append({
                'id': f'equipment_instance_{ei.id}',
                'description': f'新增设备实例：{ei.name}',
                'timestamp': timezone.localtime(ei.created_at).strftime('%Y-%m-%d %H:%M'),
                'type': 'success'
            })
        
        # 3. 故障模式最近创建记录
        failure_modes = FailureMode.objects.order_by('-created_at')[:5]
        for fm in failure_modes:
            recent_activities.append({
                'id': f'failure_mode_{fm.id}',
                'description': f'创建故障模式：{fm.name}',
                'timestamp': timezone.localtime(fm.created_at).strftime('%Y-%m-%d %H:%M'),
                'type': 'warning'
            })
        
        # 4. 危害度分析最近创建记录
        hazard_analyses = FailureModeHazardAnalysis.objects.order_by('-created_at')[:5]
        for ha in hazard_analyses:
            recent_activities.append({
                'id': f'hazard_analysis_{ha.id}',
                'description': f'完成危害度分析：{ha.failure_mode.name}',
                'timestamp': timezone.localtime(ha.created_at).strftime('%Y-%m-%d %H:%M'),
                'type': 'info'
            })
        
        # 按时间排序
        recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # 只保留最近10条记录
        recent_activities = recent_activities[:10]
        
        # 计算其他模块统计
        other_stats = {
            'total_severity_levels': SeverityLevel.objects.count(),
            'total_detection_methods': DetectionMethod.objects.count(),
            'total_compensation_measures': CompensationMeasure.objects.count(),
        }
        
        # 获取最新的分析结果
        latest_analyses = {
            'latest_failure_analysis': None,
            'latest_product_analysis': None,
        }
        
        # 最新的故障模式危害度分析
        latest_failure_analysis = FailureModeHazardAnalysis.objects.select_related(
            'failure_mode', 'severity_level'
        ).order_by('-created_at').first()
        
        if latest_failure_analysis:
            latest_analyses['latest_failure_analysis'] = {
                'id': latest_failure_analysis.id,
                'failure_mode_name': latest_failure_analysis.failure_mode.name,
                'failure_mode_code': latest_failure_analysis.failure_mode.code,
                'analysis_date': latest_failure_analysis.created_at.strftime('%Y-%m-%d'),
                'rpn_value': float(latest_failure_analysis.risk_priority_number),
                'risk_level': latest_failure_analysis.risk_level
            }
        
        # 最新的产品危害度分析
        latest_product_analysis = ProductHazardAnalysis.objects.select_related(
            'equipment_type'
        ).order_by('-analysis_date').first()
        
        if latest_product_analysis:
            latest_analyses['latest_product_analysis'] = {
                'id': latest_product_analysis.id,
                'equipment_type_name': latest_product_analysis.equipment_type.name,
                'equipment_type_code': latest_product_analysis.equipment_type.code,
                'analysis_date': latest_product_analysis.analysis_date.strftime('%Y-%m-%d'),
                'avg_rpn': float(latest_product_analysis.avg_rpn),
                'overall_risk_level': latest_product_analysis.overall_risk_level
            }
        
        # 构建概览数据
        overview_data = {
            'equipment_stats': equipment_stats,
            'failure_stats': failure_stats,
            'hazard_analysis_stats': hazard_analysis_stats,
            'other_stats': other_stats,
            'latest_analyses': latest_analyses,
            'recent_activities': recent_activities,
            'last_updated': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return Response(overview_data)
    
    @action(detail=False, methods=['get'])
    def equipment_failure_distribution(self, request):
        """设备故障分布图数据"""
        # 按设备类型统计故障模式数量
        failure_by_equipment = FailureMode.objects.values(
            'equipment_type__id', 'equipment_type__name', 'equipment_type__code'
        ).annotate(
            failure_count=Count('id'),
            analyzed_count=Count('hazard_analysis', filter=Q(hazard_analysis__is_active=True))
        ).order_by('-failure_count')
        
        # 构建响应数据
        chart_data = {
            'labels': [item['equipment_type__name'] for item in failure_by_equipment],
            'datasets': [
                {
                    'label': '故障模式总数',
                    'data': [item['failure_count'] for item in failure_by_equipment],
                    'backgroundColor': 'rgba(255, 99, 132, 0.6)'
                },
                {
                    'label': '已分析故障模式',
                    'data': [item['analyzed_count'] for item in failure_by_equipment],
                    'backgroundColor': 'rgba(54, 162, 235, 0.6)'
                }
            ]
        }
        
        return Response(chart_data)
    
    @action(detail=False, methods=['get'])
    def severity_distribution(self, request):
        """严酷度分布图数据"""
        # 按严酷度等级统计故障模式数量
        severity_distribution = FailureModeHazardAnalysis.objects.values(
            'severity_level__level', 'severity_level__name'
        ).annotate(
            count=Count('id')
        ).order_by('severity_level__level')
        
        # 构建响应数据
        chart_data = {
            'labels': [item['severity_level__name'] for item in severity_distribution],
            'datasets': [
                {
                    'label': '故障模式数量',
                    'data': [item['count'] for item in severity_distribution],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)'
                    ]
                }
            ]
        }
        
        return Response(chart_data)
    
    @action(detail=False, methods=['get'])
    def risk_level_distribution(self, request):
        """风险等级分布图数据"""
        # 按风险等级统计故障模式数量
        risk_distribution = FailureModeHazardAnalysis.objects.values(
            'risk_level'
        ).annotate(
            count=Count('id')
        )
        
        # 定义风险等级的中文名称
        risk_level_names = {
            'critical': '严重风险',
            'high': '高风险',
            'medium': '中等风险',
            'low': '低风险'
        }
        
        # 构建完整的风险等级分布数据
        full_distribution = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for item in risk_distribution:
            full_distribution[item['risk_level']] = item['count']
        
        # 构建响应数据
        chart_data = {
            'labels': [risk_level_names[key] for key in full_distribution.keys()],
            'datasets': [
                {
                    'label': '风险等级分布',
                    'data': list(full_distribution.values()),
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)'
                    ]
                }
            ]
        }
        
        return Response(chart_data)
    
    @action(detail=False, methods=['get'])
    def hazard_trend(self, request):
        """危害度趋势图数据"""
        try:
            days = int(request.query_params.get('days', 30))
        except (ValueError, TypeError):
            days = 30
        
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        rpn_trend = FailureModeHazardAnalysis.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).values(
            'created_at__date'
        ).annotate(
            avg_rpn=Avg('risk_priority_number')
        ).order_by('created_at__date')
        
        labels = [item['created_at__date'].strftime('%Y-%m-%d') for item in rpn_trend]
        data = [float(item['avg_rpn']) if item['avg_rpn'] is not None else 0 for item in rpn_trend]
        
        chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': '平均RPN值趋势',
                    'data': data,
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'tension': 0.1
                }
            ]
        }
        
        return Response(chart_data)
    
    @action(detail=False, methods=['get'])
    def top_risk_failure_modes(self, request):
        """高风险故障模式排行榜"""
        # 获取前N个高风险故障模式
        limit = int(request.query_params.get('limit', 10))
        top_failures = FailureModeHazardAnalysis.objects.select_related(
            'failure_mode', 'severity_level'
        ).order_by('-risk_priority_number')[:limit]
        
        # 构建响应数据
        top_failures_data = []
        for failure in top_failures:
            top_failures_data.append({
                'id': failure.id,
                'failure_mode_id': failure.failure_mode.id,
                'failure_mode_name': failure.failure_mode.name,
                'failure_mode_code': failure.failure_mode.code,
                'equipment_type_name': failure.failure_mode.equipment_type.name,
                'severity_level': failure.severity_level.level,
                'severity_value': float(failure.severity_value),
                'rpn_value': float(failure.risk_priority_number),
                'risk_level': failure.risk_level,
                'analysis_date': failure.created_at.strftime('%Y-%m-%d')
            })
        
        return Response(top_failures_data)
    
    @action(detail=False, methods=['get'])
    def compensation_effectiveness(self, request):
        """补偿措施有效性分析"""
        # 从故障模式与补偿措施的关联中获取数据
        compensation_by_type = FailureModeCompensation.objects.filter(
            is_active=True
        ).values(
            'compensation_measure__measure_type'
        ).annotate(
            count=Count('id'),
            avg_rating=Avg('effectiveness_rating')
        )
        
        # 补偿措施类型的中文名称
        measure_type_names = {
            'preventive': '预防性',
            'corrective': '纠正性',
            'detection': '检测性',
            'mitigation': '缓解性',
            'redundancy': '冗余性',
            'other': '其他'
        }
        
        # 构建响应数据
        chart_data = {
            'labels': [measure_type_names[item['compensation_measure__measure_type']] for item in compensation_by_type],
            'datasets': [
                {
                    'label': '使用次数',
                    'data': [item['count'] for item in compensation_by_type],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ]
                }
            ]
        }
        
        return Response(chart_data)
