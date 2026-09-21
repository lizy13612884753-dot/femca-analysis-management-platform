from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone

from .models import EquipmentType, EquipmentInstance
from .serializers import (
    EquipmentTypeSerializer, EquipmentInstanceSerializer,
    EquipmentTypeListSerializer, EquipmentInstanceListSerializer,
    EquipmentTypeSearchSerializer, EquipmentStatisticsSerializer
)
from auth_app.permissions import IsAdminOrReadOnly, IsEngineerOrAbove
from failure.pagination import CustomPageNumberPagination


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """设备类型管理视图集"""
    queryset = EquipmentType.objects.select_related('created_by').all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'category', 'manufacturer']
    search_fields = ['name', 'code', 'description', 'category', 'manufacturer']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['created_at']
    pagination_class = CustomPageNumberPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipmentTypeListSerializer
        return EquipmentTypeSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        # 添加调试日志
        print(f"DEBUG: 创建设备实例请求 - 用户: {request.user.username}")
        print(f"DEBUG: 请求数据: {request.data}")
        
        try:
            # 确保创建人字段包含在序列化数据中
            request.data['created_by'] = request.user.id
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"DEBUG: 创建设备实例失败 - 错误类型: {type(e).__name__}")
            print(f"DEBUG: 错误信息: {str(e)}")
            print(f"DEBUG: 错误详情: {e.__dict__ if hasattr(e, '__dict__') else 'N/A'}")
            raise
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索设备类型"""
        serializer = EquipmentTypeSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        query = EquipmentType.objects.select_related('created_by').all()
        validated_data = serializer.validated_data
        
        if validated_data.get('name'):
            query = query.filter(name__icontains=validated_data['name'])
        if validated_data.get('code'):
            query = query.filter(code__icontains=validated_data['code'])
        if validated_data.get('category'):
            query = query.filter(category__icontains=validated_data['category'])
        if validated_data.get('manufacturer'):
            query = query.filter(manufacturer__icontains=validated_data['manufacturer'])
        if validated_data.get('status'):
            query = query.filter(status=validated_data['status'])
        
        # 按ID升序排序
        query = query.order_by('id')
        
        result_serializer = EquipmentTypeListSerializer(query, many=True)
        return Response(result_serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取设备类型统计信息"""
        total_types = EquipmentType.objects.count()
        active_types = EquipmentType.objects.filter(status='active').count()
        
        # 按类别统计
        types_by_category = {}
        categories = EquipmentType.objects.values_list('category', flat=True).distinct()
        for category in categories:
            if category:
                count = EquipmentType.objects.filter(category=category).count()
                types_by_category[category] = count
        
        # 获取设备实例统计
        total_instances = EquipmentInstance.objects.count()
        operational_instances = EquipmentInstance.objects.filter(status='operational').count()
        maintenance_instances = EquipmentInstance.objects.filter(status='maintenance').count()
        fault_instances = EquipmentInstance.objects.filter(status='fault').count()
        
        # 设备实例按状态统计
        instances_by_status = {}
        status_choices = EquipmentInstance.STATUS_CHOICES
        for status_code, status_name in status_choices:
            count = EquipmentInstance.objects.filter(status=status_code).count()
            instances_by_status[status_name] = count
        
        data = {
            'total_types': total_types,
            'total_instances': total_instances,
            'active_types': active_types,
            'operational_instances': operational_instances,
            'maintenance_instances': maintenance_instances,
            'fault_instances': fault_instances,
            'types_by_category': types_by_category,
            'instances_by_status': instances_by_status,
        }
        
        serializer = EquipmentStatisticsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def instances(self, request, pk=None):
        """获取设备类型下的所有实例"""
        equipment_type = self.get_object()
        instances = equipment_type.instances.all()
        
        serializer = EquipmentInstanceListSerializer(instances, many=True)
        return Response(serializer.data)


class EquipmentInstanceViewSet(viewsets.ModelViewSet):
    """设备实例管理视图集"""
    queryset = EquipmentInstance.objects.select_related('equipment_type', 'created_by').all()
    permission_classes = [IsAuthenticated, IsEngineerOrAbove]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['equipment_type', 'status', 'location']
    search_fields = ['name', 'serial_number', 'location', 'function_description']
    ordering_fields = ['name', 'serial_number', 'created_at', 'equipment_type']
    ordering = ['created_at']
    serializer_class = EquipmentInstanceSerializer  # 指定用于更新操作的序列化器
    pagination_class = CustomPageNumberPagination
    
    def update(self, request, *args, **kwargs):
        # 添加详细的调试日志
        print(f"DEBUG: 更新设备实例请求 - 用户: {request.user.username}")
        print(f"DEBUG: 请求ID: {kwargs.get('pk')}")
        print(f"DEBUG: 请求数据: {request.data}")
        

        
        try:
            # 继续执行原始的更新逻辑
            response = super().update(request, *args, **kwargs)
            print(f"DEBUG: 更新成功 - 响应状态码: {response.status_code}")
            return response
        except Exception as e:
            print(f"DEBUG: 更新失败 - 错误类型: {type(e).__name__}")
            print(f"DEBUG: 错误信息: {str(e)}")
            print(f"DEBUG: 错误详情: {e.__dict__ if hasattr(e, '__dict__') else 'N/A'}")
            raise
    
    # 重写list方法，确保返回包含function_description字段的数据
    def list(self, request, *args, **kwargs):
        # 1. 获取过滤、排序后的查询集
        queryset = self.filter_queryset(self.get_queryset())
        
        # 2. 执行分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            # 3. 手动构建响应数据，确保包含function_description字段
            results = []
            for instance in page:
                result = {
                    'id': instance.id,
                    'display_id': getattr(instance, 'display_id', instance.id),
                    'equipment_type': instance.equipment_type.id,
                    'equipment_type_name': instance.equipment_type.name,
                    'equipment_type_code': instance.equipment_type.code,
                    'serial_number': instance.serial_number,
                    'name': instance.name,
                    'location': instance.location,
                    'status': instance.status,
                    'status_display': instance.get_status_display_name(),
                    'install_date': instance.install_date,
                    'warranty_expire_date': instance.warranty_expire_date,
                    'function_description': instance.function_description,  # 确保包含这个字段
                    'created_by_name': instance.created_by.username,
                    'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
                print(f"DEBUG: instance.id={instance.id}, created_at_raw={instance.created_at}, created_at_formatted={result['created_at']}")
                results.append(result)
            
            # 4. 返回分页响应
            return self.get_paginated_response(results)
        
        # 没有分页的情况
        results = []
        for instance in queryset:
            result = {
                'id': instance.id,
                'display_id': getattr(instance, 'display_id', instance.id),
                'equipment_type': instance.equipment_type.id,
                'equipment_type_name': instance.equipment_type.name,
                'equipment_type_code': instance.equipment_type.code,
                'serial_number': instance.serial_number,
                'name': instance.name,
                'location': instance.location,
                'status': instance.status,
                'status_display': instance.get_status_display_name(),
                'function_description': instance.function_description,  # 确保包含这个字段
                'created_by_name': instance.created_by.username,
                'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            results.append(result)
        
        return Response({'results': results, 'count': len(results)})
    
    def create(self, request, *args, **kwargs):
        # 添加调试日志
        print(f"创建设备实例请求 - 用户: {request.user.username}")
        print(f"请求数据: {request.data}")
        
        try:

            
            # 确保创建人字段包含在序列化数据中
            request.data['created_by'] = request.user.id
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(f"创建设备实例失败 - 错误类型: {type(e).__name__}")
            print(f"错误信息: {str(e)}")
            print(f"错误详情: {e.__dict__ if hasattr(e, '__dict__') else 'N/A'}")
            raise
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_type_id = self.request.query_params.get('equipment_type')
        if equipment_type_id:
            queryset = queryset.filter(equipment_type_id=equipment_type_id)
            
        # 处理display_id排序
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            # 如果排序字段是display_id，实际上按id排序
            if ordering == 'display_id':
                queryset = queryset.order_by('id')
            elif ordering == '-display_id':
                queryset = queryset.order_by('-id')
            # 如果按设备类型排序，相同设备类型的按创建时间排序
            elif ordering == 'equipment_type':
                queryset = queryset.order_by('equipment_type', '-created_at')
            elif ordering == '-equipment_type':
                queryset = queryset.order_by('-equipment_type', '-created_at')
            # 支持多字段排序（如：equipment_type,created_at）
            elif ',' in ordering:
                order_fields = ordering.split(',')
                queryset = queryset.order_by(*order_fields)
            else:
                queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """重写list方法，添加连续的显示ID"""
        # 获取查询集
        queryset = self.filter_queryset(self.get_queryset())
        
        # 获取分页参数
        page_number = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        # 计算偏移量
        offset = (page_number - 1) * page_size
        limit = page_size
        
        # 获取当前页数据
        page_data = list(queryset)[offset:offset + limit]
        
        # 构建响应数据
        response_data = []
        for i, instance in enumerate(page_data, 1 + offset):
            instance_dict = {
                'id': instance.id,
                'display_id': i,
                'equipment_type': instance.equipment_type.id,
                'equipment_type_name': instance.equipment_type.name,
                'equipment_type_code': instance.equipment_type.code if instance.equipment_type.code else '',
                'serial_number': instance.serial_number,
                'name': instance.name,
                'location': instance.location if instance.location else '',
                'install_date': instance.install_date.strftime('%Y-%m-%d') if instance.install_date else None,
                'warranty_expire_date': instance.warranty_expire_date.strftime('%Y-%m-%d') if instance.warranty_expire_date else None,
                'status': instance.status,
                'status_display': instance.get_status_display_name(),
                'function_description': instance.function_description if instance.function_description else '',
                'created_by_name': instance.created_by.username if instance.created_by else '',
                'created_at': timezone.localtime(instance.created_at).strftime('%Y-%m-%d %H:%M:%S')
            }
            print(f"DEBUG: id={instance.id}, created_at_raw={instance.created_at}, created_at_formatted={instance_dict['created_at']}")
            response_data.append(instance_dict)
        
        # 构建分页响应
        total = queryset.count()
        return Response({
            'count': total,
            'next': f'{request.path}?page={page_number + 1}&page_size={page_size}' if offset + limit < total else None,
            'previous': f'{request.path}?page={page_number - 1}&page_size={page_size}' if page_number > 1 else None,
            'results': response_data
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索设备实例"""
        query_params = request.query_params
        queryset = EquipmentInstance.objects.select_related('equipment_type', 'created_by').all()
        
        search_term = query_params.get('q', '')
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(serial_number__icontains=search_term) |
                Q(location__icontains=search_term)
            )
        
        equipment_type = query_params.get('equipment_type')
        if equipment_type:
            queryset = queryset.filter(equipment_type_id=equipment_type)
        
        status = query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # 按设备类型和序列号排序
        queryset = queryset.order_by('equipment_type', 'serial_number')
        
        # 序列化数据
        serializer = EquipmentInstanceListSerializer(queryset, many=True)
        data = serializer.data
        
        # 在响应数据中添加display_id
        for i, item in enumerate(data, 1):
            item['display_id'] = i
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新设备实例状态"""
        instance = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(EquipmentInstance.STATUS_CHOICES):
            return Response(
                {'error': '无效的状态值'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.status = new_status
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_with_display_id(self, request):
        """获取带显示ID的设备实例列表"""
        # 获取所有设备实例，按设备类型和序列号排序
        queryset = EquipmentInstance.objects.select_related('equipment_type').all()
        queryset = queryset.order_by('equipment_type', 'serial_number')
        
        # 生成连续的显示ID
        instances = list(queryset)
        for i, instance in enumerate(instances, 1):
            # 使用动态属性添加显示ID
            instance.display_id = i
        
        # 使用列表序列化器返回数据
        serializer = EquipmentInstanceListSerializer(instances, many=True)
        
        # 在返回结果中添加display_id字段
        data = serializer.data
        for i, item in enumerate(data):
            item['display_id'] = i + 1
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """按设备类型分组获取实例"""
        equipment_type_id = request.query_params.get('equipment_type')
        if not equipment_type_id:
            return Response(
                {'error': '必须提供设备类型ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instances = EquipmentInstance.objects.filter(
            equipment_type_id=equipment_type_id
        )
        
        serializer = EquipmentInstanceListSerializer(instances, many=True)
        return Response(serializer.data)