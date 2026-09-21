from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EquipmentType(models.Model):
    """设备类型模型"""
    STATUS_CHOICES = [
        ('active', '活跃'),
        ('inactive', '不活跃'),
        ('archived', '已归档'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name='设备类型名称')
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='设备类型编码')
    description = models.TextField(blank=True, verbose_name='设备类型描述')
    category = models.CharField(max_length=100, blank=True, verbose_name='设备类别')
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='制造商')
    model = models.CharField(max_length=100, blank=True, verbose_name='型号')
    specifications = models.JSONField(default=dict, verbose_name='技术规格')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active', 
        verbose_name='状态'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'equipment_types'
        verbose_name = '设备类型'
        verbose_name_plural = '设备类型'

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_status_display_name(self):
        """获取状态显示名称"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class EquipmentInstance(models.Model):
    """设备实例模型"""
    STATUS_CHOICES = [
        ('operational', '运行中'),
        ('maintenance', '维护中'),
        ('fault', '故障'),
        ('offline', '离线'),
        ('decommissioned', '已退役'),
    ]
    
    equipment_type = models.ForeignKey(
        EquipmentType, 
        on_delete=models.CASCADE, 
        related_name='instances',
        verbose_name='设备类型'
    )
    serial_number = models.CharField(max_length=100, verbose_name='序列号')
    name = models.CharField(max_length=200, verbose_name='设备名称')
    location = models.CharField(max_length=200, blank=True, verbose_name='安装位置')
    install_date = models.DateField(null=True, blank=True, verbose_name='安装日期')
    warranty_expire_date = models.DateField(null=True, blank=True, verbose_name='保修到期日期')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='operational', 
        verbose_name='状态'
    )
    custom_specifications = models.JSONField(default=dict, verbose_name='自定义规格')
    function_description = models.TextField(blank=True, verbose_name='功能描述')
    notes = models.TextField(blank=True, verbose_name='备注')
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'equipment_instances'
        verbose_name = '设备实例'
        verbose_name_plural = '设备实例'
        ordering = ['equipment_type', 'serial_number']
        unique_together = [['equipment_type', 'serial_number']]

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
    
    def get_status_display_name(self):
        """获取状态显示名称"""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)