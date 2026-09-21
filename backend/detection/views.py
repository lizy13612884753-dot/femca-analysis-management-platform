from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone

from .models import DetectionMethod, DetectionRating, FailureModeDetection
from .serializers import (
    DetectionMethodSerializer, DetectionRatingSerializer, FailureModeDetectionSerializer,
    DetectionMethodListSerializer, DetectionRatingListSerializer, FailureModeDetectionListSerializer,
    DetectionMethodSearchSerializer, FailureModeDetectionSearchSerializer
)
from auth_app.permissions import IsAdminOrReadOnly, IsEngineerOrAbove


class DetectionMethodViewSet(viewsets.ModelViewSet):
    """检测方法管理视图集"""
    queryset = DetectionMethod.objects.all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['method_type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DetectionMethodListSerializer
        return DetectionMethodSerializer
    
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
        """搜索检测方法"""
        serializer = DetectionMethodSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = DetectionMethod.objects.all()
        validated_data = serializer.validated_data
        
        if validated_data.get('name'):
            query = query.filter(name__icontains=validated_data['name'])
        if validated_data.get('code'):
            query = query.filter(code__icontains=validated_data['code'])
        if validated_data.get('method_type'):
            query = query.filter(method_type=validated_data['method_type'])
        if validated_data.get('equipment_type'):
            query = query.filter(equipment_types__id=validated_data['equipment_type'])
        if validated_data.get('is_active') is not None:
            query = query.filter(is_active=validated_data['is_active'])
        
        result_serializer = DetectionMethodListSerializer(query, many=True)
        return Response(result_serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_equipment_type(self, request):
        """获取指定设备类型的检测方法"""
        equipment_type_id = request.query_params.get('equipment_type')
        if not equipment_type_id:
            return Response(
                {'error': '必须提供设备类型ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        methods = DetectionMethod.objects.filter(
            equipment_types__id=equipment_type_id
        ).distinct()
        
        serializer = DetectionMethodListSerializer(methods, many=True)
        return Response(serializer.data)


class DetectionRatingViewSet(viewsets.ModelViewSet):
    """检测评级管理视图集"""
    queryset = DetectionRating.objects.all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'is_active']
    ordering_fields = ['rpn_score', 'rating']
    ordering = ['rpn_score']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DetectionRatingListSerializer
        return DetectionRatingSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """获取激活的检测评级"""
        ratings = DetectionRating.objects.filter(is_active=True).order_by('rpn_score')
        serializer = DetectionRatingListSerializer(ratings, many=True)
        return Response(serializer.data)


class FailureModeDetectionViewSet(viewsets.ModelViewSet):
    """故障模式检测关联管理视图集"""
    queryset = FailureModeDetection.objects.select_related(
        'failure_mode', 'detection_method', 'detection_rating'
    ).all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['failure_mode', 'detection_method', 'detection_rating', 'is_active']
    search_fields = ['notes']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FailureModeDetectionListSerializer
        return FailureModeDetectionSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索故障模式检测关联"""
        serializer = FailureModeDetectionSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = FailureModeDetection.objects.select_related(
            'failure_mode', 'detection_method', 'detection_rating'
        ).all()
        validated_data = serializer.validated_data
        
        if validated_data.get('failure_mode'):
            query = query.filter(failure_mode_id=validated_data['failure_mode'])
        if validated_data.get('detection_method'):
            query = query.filter(detection_method_id=validated_data['detection_method'])
        if validated_data.get('detection_rating'):
            query = query.filter(detection_rating_id=validated_data['detection_rating'])
        if validated_data.get('is_active') is not None:
            query = query.filter(is_active=validated_data['is_active'])
        
        result_serializer = FailureModeDetectionListSerializer(query, many=True)
        return Response(result_serializer.data)
    
    @action(detail=True, methods=['get'])
    def detection_analysis(self, request, pk=None):
        """获取检测分析的详细信息"""
        detection = self.get_object()
        
        # 计算总成本和时间
        total_cost = detection.detection_method.cost
        total_time = detection.detection_method.time_required
        detection_score = detection.detection_rating.rpn_score
        
        # 构建分析数据
        analysis_data = {
            'failure_mode': {
                'id': detection.failure_mode.id,
                'name': detection.failure_mode.name,
                'code': detection.failure_mode.code,
                'description': detection.failure_mode.description
            },
            'detection_method': {
                'id': detection.detection_method.id,
                'name': detection.detection_method.name,
                'code': detection.detection_method.code,
                'description': detection.detection_method.description,
                'method_type': detection.detection_method.method_type,
                'cost': float(detection.detection_method.cost),
                'time_required': detection.detection_method.time_required,
                'accuracy': detection.detection_method.accuracy
            },
            'detection_rating': {
                'rating': detection.detection_rating.rating,
                'name': detection.detection_rating.name,
                'description': detection.detection_rating.description,
                'rpn_score': detection.detection_rating.rpn_score
            },
            'analysis': {
                'total_cost': float(total_cost),
                'total_time': total_time,
                'detection_score': detection_score,
                'risk_level': self._get_risk_level(detection_score)
            }
        }
        
        return Response(analysis_data)
    
    def _get_risk_level(self, rpn_score):
        """根据RPN分数获取风险等级"""
        if rpn_score <= 2:
            return '低'
        elif rpn_score <= 5:
            return '中'
        elif rpn_score <= 7:
            return '高'
        else:
            return '极高'
    
    @action(detail=True, methods=['post'])
    def update_rating(self, request, pk=None):
        """更新检测评级"""
        detection = self.get_object()
        rating_id = request.data.get('detection_rating')
        
        if not rating_id:
            return Response(
                {'error': '必须提供评级ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            rating = DetectionRating.objects.get(id=rating_id, is_active=True)
            detection.detection_rating = rating
            detection.save()
            
            serializer = self.get_serializer(detection)
            return Response(serializer.data)
        except DetectionRating.DoesNotExist:
            return Response(
                {'error': '无效的评级ID或评级未激活'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def for_failure_mode(self, request):
        """获取指定故障模式的所有检测方法"""
        failure_mode_id = request.query_params.get('failure_mode')
        if not failure_mode_id:
            return Response(
                {'error': '必须提供故障模式ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        detections = FailureModeDetection.objects.filter(
            failure_mode_id=failure_mode_id,
            is_active=True
        ).select_related('detection_method', 'detection_rating')
        
        serializer = FailureModeDetectionListSerializer(detections, many=True)
        return Response(serializer.data)