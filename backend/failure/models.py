from django.db import models
from django.contrib.auth import get_user_model
from equipment.models import EquipmentType

User = get_user_model()


class FailureCause(models.Model):
    """故障原因模型"""
    name = models.CharField(max_length=100, verbose_name='故障原因名称')
    description = models.TextField(blank=True, verbose_name='故障原因描述')
    failure_mode = models.ForeignKey(
        'FailureMode',
        on_delete=models.CASCADE,
        related_name='failure_causes',
        verbose_name='关联故障模式'
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
        db_table = 'failure_causes'
        verbose_name = '故障原因'
        verbose_name_plural = '故障原因'
        ordering = ['name']

    def __str__(self):
        return self.name


class FailureEffect(models.Model):
    """故障影响模型"""
    name = models.CharField(max_length=100, verbose_name='故障影响名称')
    description = models.TextField(blank=True, verbose_name='故障影响描述')
    failure_mode = models.ForeignKey(
        'FailureMode',
        on_delete=models.CASCADE,
        related_name='failure_effects',
        verbose_name='关联故障模式'
    )
    severity = models.CharField(
        max_length=1,
        choices=[
            ('A', '极高'),
            ('B', '高'),
            ('C', '中等'),
            ('D', '低'),
            ('E', '极低'),
        ],
        verbose_name='影响严重性'
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
        db_table = 'failure_effects'
        verbose_name = '故障影响'
        verbose_name_plural = '故障影响'
        ordering = ['severity', 'name']

    def __str__(self):
        return self.name


class FailureMode(models.Model):
    """故障模式模型"""
    # 严重性等级
    SEVERITY_CHOICES = [
        ('A', '极高'),
        ('B', '高'),
        ('C', '中等'),
        ('D', '低'),
        ('E', '极低'),
    ]
    
    # 功能状态
    FUNCTION_STATUS_CHOICES = [
        ('1', '丧失功能'),
        ('2', '功能降级'),
        ('3', '功能无影响'),
    ]
    
    # 严重性等级评分
    SEVERITY_SCORES = {
        'A': 10,  # 极高
        'B': 6,   # 高
        'C': 3,   # 中等
        'D': 1,   # 低
        'E': 0.5, # 极低
    }
    
    name = models.CharField(max_length=100, verbose_name='故障模式名称')
    code = models.CharField(max_length=50, verbose_name='故障模式编码')
    description = models.TextField(blank=True, verbose_name='故障模式描述')
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='failure_modes',
        verbose_name='设备类型'
    )
    function_name = models.CharField(max_length=100, verbose_name='功能名称')
    function_status = models.CharField(
        max_length=1,
        choices=FUNCTION_STATUS_CHOICES,
        verbose_name='功能状态'
    )
    failure_effect = models.TextField(verbose_name='故障影响')
    severity = models.CharField(
        max_length=1,
        choices=SEVERITY_CHOICES,
        verbose_name='严重性等级'
    )
    severity_score = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name='严重性分数')
    occurrence_rate = models.PositiveIntegerField(default=0, verbose_name='发生频率(%)')
    frequency = models.CharField(max_length=50, blank=True, verbose_name='发生频率描述')
    causes = models.TextField(blank=True, verbose_name='故障原因')
    detection_methods = models.TextField(blank=True, verbose_name='检测方法')
    notes = models.TextField(blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='创建人'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'failure_modes'
        verbose_name = '故障模式'
        verbose_name_plural = '故障模式'
        ordering = ['equipment_type', 'severity_score']

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        """保存时自动设置严重性分数"""
        if self.severity in self.SEVERITY_SCORES:
            self.severity_score = self.SEVERITY_SCORES[self.severity]
        super().save(*args, **kwargs)