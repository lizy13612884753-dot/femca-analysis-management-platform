from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import CompensationMeasure, EffectivenessEvaluation, FailureModeCompensation
from .serializers import (
    CompensationMeasureSerializer, EffectivenessEvaluationSerializer, FailureModeCompensationSerializer,
    CompensationMeasureListSerializer, EffectivenessEvaluationListSerializer, FailureModeCompensationListSerializer,
    CompensationMeasureSearchSerializer, EffectivenessEvaluationSearchSerializer, FailureModeCompensationSearchSerializer
)
from auth_app.permissions import IsAdminOrReadOnly, IsEngineerOrAbove


class CompensationMeasureViewSet(viewsets.ModelViewSet):
    """补偿措施管理视图集"""
    queryset = CompensationMeasure.objects.all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['measure_type', 'implementation_complexity', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompensationMeasureListSerializer
        return CompensationMeasureSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_type_id = self.request.query_params.get('equipment_type')
        if equipment_type_id:
            queryset = queryset.filter(equipment_types__id=equipment_type_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索补偿措施"""
        serializer = CompensationMeasureSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = CompensationMeasure.objects.all()
        validated_data = serializer.validated_data
        
        if validated_data.get('name'):
            query = query.filter(name__icontains=validated_data['name'])
        if validated_data.get('code'):
            query = query.filter(code__icontains=validated_data['code'])
        if validated_data.get('measure_type'):
            query = query.filter(measure_type=validated_data['measure_type'])
        if validated_data.get('equipment_type'):
            query = query.filter(equipment_types__id=validated_data['equipment_type'])
        if validated_data.get('implementation_complexity'):
            query = query.filter(implementation_complexity=validated_data['implementation_complexity'])
        if validated_data.get('is_active') is not None:
            query = query.filter(is_active=validated_data['is_active'])
        
        result_serializer = CompensationMeasureListSerializer(query, many=True)
        return Response(result_serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_equipment_type(self, request):
        """获取指定设备类型的补偿措施"""
        equipment_type_id = request.query_params.get('equipment_type')
        if not equipment_type_id:
            return Response(
                {'error': '必须提供设备类型ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        measures = CompensationMeasure.objects.filter(
            equipment_types__id=equipment_type_id
        ).distinct()
        
        serializer = CompensationMeasureListSerializer(measures, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def effectiveness_analysis(self, request, pk=None):
        """获取补偿措施的效果分析"""
        measure = self.get_object()
        
        # 获取所有有效性评估
        evaluations = EffectivenessEvaluation.objects.filter(
            compensation_measure=measure,
            is_active=True
        ).select_related('evaluator')
        
        # 计算统计数据
        effectiveness_data = {
            'compensation_measure': {
                'id': measure.id,
                'name': measure.name,
                'code': measure.code,
                'expected_effectiveness': measure.effectiveness
            },
            'evaluation_stats': {
                'total_evaluations': evaluations.count(),
                'average_effectiveness': 0,
                'min_effectiveness': 0,
                'max_effectiveness': 0,
                'latest_evaluation': None
            },
            'evaluations': []
        }
        
        if evaluations.exists():
            avg_effectiveness = evaluations.aggregate(avg=Avg('actual_effectiveness'))['avg']
            min_effectiveness = evaluations.order_by('actual_effectiveness').first().actual_effectiveness
            max_effectiveness = evaluations.order_by('-actual_effectiveness').first().actual_effectiveness
            latest_evaluation = evaluations.order_by('-evaluation_date').first()
            
            effectiveness_data['evaluation_stats']['average_effectiveness'] = float(avg_effectiveness)
            effectiveness_data['evaluation_stats']['min_effectiveness'] = float(min_effectiveness)
            effectiveness_data['evaluation_stats']['max_effectiveness'] = float(max_effectiveness)
            effectiveness_data['evaluation_stats']['latest_evaluation'] = {
                'date': latest_evaluation.evaluation_date.strftime('%Y-%m-%d'),
                'evaluator': latest_evaluation.evaluator.username if latest_evaluation.evaluator else None,
                'effectiveness': float(latest_evaluation.actual_effectiveness)
            }
            
            # 添加最近几次评估数据
            recent_evaluations = evaluations.order_by('-evaluation_date')[:5]
            effectiveness_data['evaluations'] = [
                {
                    'date': eval.evaluation_date.strftime('%Y-%m-%d'),
                    'evaluator': eval.evaluator.username if eval.evaluator else None,
                    'effectiveness': float(eval.actual_effectiveness),
                    'notes': eval.notes
                }
                for eval in recent_evaluations
            ]
        
        return Response(effectiveness_data)


class EffectivenessEvaluationViewSet(viewsets.ModelViewSet):
    """有效性评估管理视图集"""
    queryset = EffectivenessEvaluation.objects.select_related(
        'compensation_measure', 'evaluator'
    ).all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['compensation_measure', 'evaluator', 'is_active']
    search_fields = ['notes']
    ordering_fields = ['evaluation_date', 'actual_effectiveness']
    ordering = ['-evaluation_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EffectivenessEvaluationListSerializer
        return EffectivenessEvaluationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索有效性评估"""
        serializer = EffectivenessEvaluationSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = EffectivenessEvaluation.objects.select_related(
            'compensation_measure', 'evaluator'
        ).all()
        validated_data = serializer.validated_data
        
        if validated_data.get('compensation_measure'):
            query = query.filter(compensation_measure_id=validated_data['compensation_measure'])
        if validated_data.get('evaluator'):
            query = query.filter(evaluator_id=validated_data['evaluator'])
        if validated_data.get('start_date'):
            query = query.filter(evaluation_date__gte=validated_data['start_date'])
        if validated_data.get('end_date'):
            query = query.filter(evaluation_date__lte=validated_data['end_date'])
        if validated_data.get('is_active') is not None:
            query = query.filter(is_active=validated_data['is_active'])
        
        result_serializer = EffectivenessEvaluationListSerializer(query, many=True)
        return Response(result_serializer.data)
    
    @action(detail=False, methods=['get'])
    def for_compensation(self, request):
        """获取指定补偿措施的所有评估"""
        compensation_id = request.query_params.get('compensation_measure')
        if not compensation_id:
            return Response(
                {'error': '必须提供补偿措施ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evaluations = EffectivenessEvaluation.objects.filter(
            compensation_measure_id=compensation_id,
            is_active=True
        ).select_related('evaluator')
        
        serializer = EffectivenessEvaluationListSerializer(evaluations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent_evaluations(self, request):
        """获取最近的评估"""
        days = int(request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        evaluations = EffectivenessEvaluation.objects.filter(
            evaluation_date__gte=start_date,
            evaluation_date__lte=end_date,
            is_active=True
        ).select_related('compensation_measure', 'evaluator').order_by('-evaluation_date')
        
        serializer = EffectivenessEvaluationListSerializer(evaluations, many=True)
        return Response(serializer.data)


class FailureModeCompensationViewSet(viewsets.ModelViewSet):
    """故障模式补偿关联管理视图集"""
    queryset = FailureModeCompensation.objects.select_related(
        'failure_mode', 'compensation_measure'
    ).all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['failure_mode', 'compensation_measure', 'effectiveness_rating', 'is_active']
    search_fields = ['notes']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FailureModeCompensationListSerializer
        return FailureModeCompensationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索故障模式补偿关联"""
        serializer = FailureModeCompensationSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = FailureModeCompensation.objects.select_related(
            'failure_mode', 'compensation_measure'
        ).all()
        validated_data = serializer.validated_data
        
        if validated_data.get('failure_mode'):
            query = query.filter(failure_mode_id=validated_data['failure_mode'])
        if validated_data.get('compensation_measure'):
            query = query.filter(compensation_measure_id=validated_data['compensation_measure'])
        if validated_data.get('effectiveness_rating'):
            query = query.filter(effectiveness_rating=validated_data['effectiveness_rating'])
        if validated_data.get('is_active') is not None:
            query = query.filter(is_active=validated_data['is_active'])
        
        result_serializer = FailureModeCompensationListSerializer(query, many=True)
        return Response(result_serializer.data)
    
    @action(detail=True, methods=['get'])
    def effectiveness_analysis(self, request, pk=None):
        """获取补偿措施效果分析的详细信息"""
        compensation = self.get_object()
        
        # 获取补偿措施的效果评估
        evaluations = EffectivenessEvaluation.objects.filter(
            compensation_measure=compensation.compensation_measure,
            is_active=True
        )
        
        # 计算统计数据
        effectiveness_data = {
            'failure_mode': {
                'id': compensation.failure_mode.id,
                'name': compensation.failure_mode.name,
                'code': compensation.failure_mode.code
            },
            'compensation_measure': {
                'id': compensation.compensation_measure.id,
                'name': compensation.compensation_measure.name,
                'code': compensation.compensation_measure.code,
                'type': compensation.compensation_measure.get_measure_type_display_name(),
                'expected_effectiveness': compensation.compensation_measure.effectiveness,
                'cost': float(compensation.compensation_measure.cost),
                'implementation_complexity': compensation.compensation_measure.get_complexity_display_name()
            },
            'rating': {
                'value': compensation.effectiveness_rating,
                'display': compensation.get_rating_display_name()
            },
            'analysis': {
                'is_effective': self._is_effective(compensation.effectiveness_rating),
                'notes': compensation.notes,
                'effectiveness_history': []
            }
        }
        
        # 添加历史效果数据
        if evaluations.exists():
            effectiveness_data['analysis']['effectiveness_history'] = [
                {
                    'date': eval.evaluation_date.strftime('%Y-%m-%d'),
                    'effectiveness': float(eval.actual_effectiveness)
                }
                for eval in evaluations.order_by('-evaluation_date')[:5]
            ]
        
        return Response(effectiveness_data)
    
    def _is_effective(self, rating):
        """判断补偿措施是否有效"""
        effective_ratings = ['A', 'B', 'C']
        return rating in effective_ratings
    
    @action(detail=False, methods=['get'])
    def for_failure_mode(self, request):
        """获取指定故障模式的所有补偿措施"""
        failure_mode_id = request.query_params.get('failure_mode')
        if not failure_mode_id:
            return Response(
                {'error': '必须提供故障模式ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compensations = FailureModeCompensation.objects.filter(
            failure_mode_id=failure_mode_id,
            is_active=True
        ).select_related('compensation_measure')
        
        serializer = FailureModeCompensationListSerializer(compensations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def for_compensation(self, request):
        """获取指定补偿措施的所有故障模式"""
        compensation_id = request.query_params.get('compensation_measure')
        if not compensation_id:
            return Response(
                {'error': '必须提供补偿措施ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compensations = FailureModeCompensation.objects.filter(
            compensation_measure_id=compensation_id,
            is_active=True
        ).select_related('failure_mode')
        
        serializer = FailureModeCompensationListSerializer(compensations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_rating(self, request, pk=None):
        """更新补偿措施评级"""
        compensation = self.get_object()
        rating = request.data.get('effectiveness_rating')
        
        if not rating:
            return Response(
                {'error': '必须提供评级'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 验证评级是否有效
        if rating not in dict(FailureModeCompensation.RATING_CHOICES):
            return Response(
                {'error': '无效的评级'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        compensation.effectiveness_rating = rating
        compensation.save()
        
        serializer = self.get_serializer(compensation)
        return Response(serializer.data)