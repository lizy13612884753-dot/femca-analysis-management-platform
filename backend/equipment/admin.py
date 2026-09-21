from django.contrib import admin
from .models import EquipmentType, EquipmentInstance


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    """设备类型管理界面"""
    list_display = ['name', 'code', 'category', 'manufacturer', 'model', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'category', 'manufacturer', 'created_at']
    search_fields = ['name', 'code', 'description', 'category', 'manufacturer', 'model']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'code', 'description')
        }),
        ('技术信息', {
            'fields': ('category', 'manufacturer', 'model', 'specifications')
        }),
        ('状态信息', {
            'fields': ('status',)
        }),
        ('创建信息', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EquipmentInstance)
class EquipmentInstanceAdmin(admin.ModelAdmin):
    """设备实例管理界面"""
    list_display = ['name', 'serial_number', 'equipment_type', 'location', 'status', 'install_date', 'created_by', 'created_at']
    list_filter = ['status', 'equipment_type', 'install_date', 'created_at']
    search_fields = ['name', 'serial_number', 'location']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'install_date'
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'serial_number', 'equipment_type', 'location')
        }),
        ('时间信息', {
            'fields': ('install_date', 'warranty_expire_date')
        }),
        ('状态信息', {
            'fields': ('status',)
        }),
        ('自定义信息', {
            'fields': ('custom_specifications', 'notes'),
            'classes': ('collapse',)
        }),
        ('创建信息', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)