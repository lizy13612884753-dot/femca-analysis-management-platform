from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import SeverityLevel, SeverityIndicator, SeverityAssessment
from .serializers import (
    SeverityLevelSerializer,
    SeverityIndicatorSerializer,
    SeverityAssessmentSerializer
)
from .permissions import IsAdminOrReadOnly


class SeverityLevelViewSet(viewsets.ModelViewSet):
    """严酷度等级管理视图集"""
    queryset = SeverityLevel.objects.select_related('created_by').all()
    serializer_class = SeverityLevelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['level', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['level', 'score', 'created_at']
    ordering = ['score']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 过滤出用户有权限访问的严酷度等级
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看启用的严酷度等级
            queryset = queryset.filter(is_active=True)
        
        return queryset


class SeverityIndicatorViewSet(viewsets.ModelViewSet):
    """严酷度指标管理视图集"""
    queryset = SeverityIndicator.objects.select_related('created_by').all()
    serializer_class = SeverityIndicatorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]


class SeverityAssessmentViewSet(viewsets.ModelViewSet):
    """严酷度评定管理视图集"""
    queryset = SeverityAssessment.objects.select_related(
        'failure_mode', 'severity_level', 'created_by'
    ).all()
    serializer_class = SeverityAssessmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['failure_mode', 'severity_level', 'is_active']
    # 搜索字段
    search_fields = ['project_instance_name', 'evaluation', 'evidence', 'failure_mode__name', 'created_by__username']
    ordering_fields = ['score', 'created_at']
    ordering = ['created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 过滤出用户有权限访问的严酷度评定
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看自己创建的严酷度评定
            queryset = queryset.filter(created_by=user)
        
        return queryset
