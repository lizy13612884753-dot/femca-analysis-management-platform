from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """管理员或只读权限"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and (request.user.is_staff or request.user.role == 'admin')


class IsOwnerOrAdmin(permissions.BasePermission):
    """用户本人或管理员权限"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.role == 'admin':
            return True
        return hasattr(obj, 'user') and obj.user == request.user


class IsAdmin(permissions.BasePermission):
    """仅管理员权限"""
    
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.role == 'admin')


class IsManagerOrAdmin(permissions.BasePermission):
    """管理员或项目经理权限"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'manager'] or request.user.is_staff


class IsEngineerOrAbove(permissions.BasePermission):
    """工程师及以上权限"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'manager', 'engineer'] or request.user.is_staff