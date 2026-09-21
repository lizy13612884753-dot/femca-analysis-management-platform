from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, CustomRole, CustomPermission


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    """用户管理界面"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'status', 'is_active', 'last_login_time', 'date_joined']
    list_filter = ['role', 'status', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['last_login_time', 'date_joined', 'last_login_ip']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {
            'fields': ('role', 'status', 'phone', 'department', 'last_login_ip', 'last_login_time')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter()


@admin.register(CustomRole)
class RoleAdmin(admin.ModelAdmin):
    """角色管理界面"""
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CustomPermission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理界面"""
    list_display = ['name', 'code', 'module', 'created_at']
    list_filter = ['module']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at']