from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """管理员或只读权限"""
    def has_permission(self, request, view):
        # 所有请求都允许读取权限
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 只有管理员或超级用户可以修改
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin')


class IsOwnerOrAdmin(permissions.BasePermission):
    """资源所有者或管理员权限"""
    def has_object_permission(self, request, view, obj):
        # 所有请求都允许读取权限
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 资源所有者或管理员可以修改
        return obj.created_by == request.user or request.user.is_superuser or request.user.role == 'admin'
