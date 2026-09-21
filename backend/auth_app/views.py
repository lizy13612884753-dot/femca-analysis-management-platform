from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import CustomUser, CustomRole, CustomPermission
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer, 
    UserDetailSerializer, RoleSerializer, PermissionSerializer,
    ChangePasswordSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


User = get_user_model()


class RegisterViewSet(viewsets.GenericViewSet):
    """用户注册视图集"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        """用户注册"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 生成token
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginViewSet(viewsets.GenericViewSet, TokenObtainPairView):
    """用户登录视图集"""
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        """用户登录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # 更新登录信息
        user.update_last_login_info(self.get_client_ip(request))
        
        # 生成token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutViewSet(viewsets.GenericViewSet):
    """用户退出登录视图集"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """退出登录"""
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': '退出成功'})
        except Exception as e:
            return Response({'message': '退出失败'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'status', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login_time', 'username']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'admin':
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """获取当前用户信息"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """修改密码"""
        serializer = ChangePasswordSerializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': '密码修改成功'})
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """搜索用户"""
        query = request.query_params.get('q', '')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        else:
            users = User.objects.none()
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """角色管理视图集"""
    queryset = CustomRole.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly()]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class PermissionViewSet(viewsets.ModelViewSet):
    """权限管理视图集"""
    queryset = CustomPermission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly()]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['module', 'code']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'module', 'created_at']
    ordering = ['module', 'name']