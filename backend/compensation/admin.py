from django.contrib import admin
from .models import CompensationMeasure, EffectivenessEvaluation, FailureModeCompensation


@admin.register(CompensationMeasure)
class CompensationMeasureAdmin(admin.ModelAdmin):
    """补偿措施管理界面"""
    list_display = ['name', 'code', 'measure_type', 'implementation_complexity', 'effectiveness', 'is_active', 'created_by', 'created_at']
    list_filter = ['measure_type', 'implementation_complexity', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ('equipment_types',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'code', 'description')
        }),
        ('类型和复杂性', {
            'fields': ('measure_type', 'implementation_complexity')
        }),
        ('效果信息', {
            'fields': ('effectiveness',)
        }),
        ('资源需求', {
            'fields': ('cost', 'time_required')
        }),
        ('适用设备类型', {
            'fields': ('equipment_types',)
        }),
        ('状态信息', {
            'fields': ('is_active',)
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


@admin.register(EffectivenessEvaluation)
class EffectivenessEvaluationAdmin(admin.ModelAdmin):
    """有效性评估管理界面"""
    list_display = ['compensation_measure', 'evaluation_date', 'evaluator', 'actual_effectiveness', 'is_active', 'created_at']
    list_filter = ['evaluation_date', 'is_active', 'created_at']
    search_fields = ['compensation_measure__name', 'evaluator__username', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'evaluation_date'
    fieldsets = (
        ('基本信息', {
            'fields': ('compensation_measure', 'evaluation_date', 'evaluator')
        }),
        ('评估结果', {
            'fields': ('actual_effectiveness', 'notes')
        }),
        ('状态信息', {
            'fields': ('is_active',)
        }),
        ('创建信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FailureModeCompensation)
class FailureModeCompensationAdmin(admin.ModelAdmin):
    """故障模式补偿关联管理界面"""
    list_display = ['failure_mode', 'compensation_measure', 'effectiveness_rating', 'is_active', 'created_by', 'created_at']
    list_filter = ['effectiveness_rating', 'is_active', 'created_at']
    search_fields = ['failure_mode__name', 'compensation_measure__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('关联信息', {
            'fields': ('failure_mode', 'compensation_measure')
        }),
        ('评估结果', {
            'fields': ('effectiveness_rating', 'notes')
        }),
        ('状态信息', {
            'fields': ('is_active',)
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