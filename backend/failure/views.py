from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import FailureMode, FailureCause, FailureEffect
from .serializers import (
    FailureModeSerializer,
    FailureModeListSerializer,
    FailureCauseSerializer,
    FailureEffectSerializer
)
from .permissions import IsAdminOrReadOnly
from .pagination import CustomPageNumberPagination


class FailureModeViewSet(viewsets.ModelViewSet):
    """故障模式管理视图集"""
    queryset = FailureMode.objects.select_related('equipment_type', 'created_by').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['equipment_type', 'severity', 'function_status', 'is_active']
    search_fields = ['name', 'code', 'description', 'function_name', 'equipment_type__name', 'created_by__username']
    ordering_fields = ['name', 'code', 'created_at', 'severity']
    ordering = ['created_at']
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return FailureModeListSerializer
        return FailureModeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 过滤出用户有权限访问的故障模式
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看自己创建的故障模式
            queryset = queryset.filter(created_by=user)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """创建故障模式"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FailureCauseViewSet(viewsets.ModelViewSet):
    """故障原因管理视图集"""
    queryset = FailureCause.objects.select_related('failure_mode', 'created_by').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['failure_mode']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    serializer_class = FailureCauseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 过滤出用户有权限访问的故障原因
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看自己创建的故障原因
            queryset = queryset.filter(created_by=user)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """创建故障原因"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FailureEffectViewSet(viewsets.ModelViewSet):
    """故障影响管理视图集"""
    queryset = FailureEffect.objects.select_related('failure_mode', 'created_by').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['failure_mode', 'severity']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'severity', 'created_at']
    ordering = ['severity', 'name']

    serializer_class = FailureEffectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # 过滤出用户有权限访问的故障影响
        if not user.is_superuser and user.role != 'admin':
            # 普通用户只能查看自己创建的故障影响
            queryset = queryset.filter(created_by=user)
        
        return queryset

    def create(self, request, *args, **kwargs):
        """创建故障影响"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
