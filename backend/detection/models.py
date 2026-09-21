from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DetectionMethod(models.Model):
    """检测方法模型"""
    METHOD_TYPE_CHOICES = [
        ('inspection', '检测'),
        ('monitoring', '监控'),
        ('testing', '测试'),
        ('other', '其他'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name='检测方法名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='检测方法编码')
    description = models.TextField(blank=True, verbose_name='检测方法描述')
    method_type = models.CharField(
        max_length=20, 
        choices=METHOD_TYPE_CHOICES, 
        default='inspection', 
        verbose_name='方法类型'
    )
    equipment_types = models.ManyToManyField(
        'equipment.EquipmentType',
        blank=True,
        verbose_name='适用设备类型'
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='成本')
    time_required = models.PositiveIntegerField(default=0, verbose_name='所需时间（分钟）')
    accuracy = models.FloatField(default=0.95, verbose_name='准确率（0-1）')
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
        db_table = 'detection_methods'
        verbose_name = '检测方法'
        verbose_name_plural = '检测方法'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_method_type_display_name(self):
        """获取方法类型显示名称"""
        return dict(self.METHOD_TYPE_CHOICES).get(self.method_type, self.method_type)


class DetectionRating(models.Model):
    """检测评级模型"""
    RATING_CHOICES = [
        ('A', 'A - 几乎确定'),
        ('B', 'B - 非常高'),
        ('C', 'C - 高'),
        ('D', 'D - 中等'),
        ('E', 'E - 低'),
        ('F', 'F - 非常低'),
        ('G', 'G - 几乎不可能'),
    ]
    
    RPN_SCORES = {
        'A': 1,  # 几乎确定
        'B': 2,  # 非常高
        'C': 3,  # 高
        'D': 4,  # 中等
        'E': 5,  # 低
        'F': 8,  # 非常低
        'G': 10, # 几乎不可能
    }
    
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, verbose_name='检测等级')
    name = models.CharField(max_length=50, verbose_name='等级名称')
    description = models.TextField(blank=True, verbose_name='等级描述')
    rpn_score = models.IntegerField(default=1, verbose_name='RPN分数')
    detection_time = models.PositiveIntegerField(default=0, verbose_name='检测时间（分钟）')
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
        db_table = 'detection_ratings'
        verbose_name = '检测评级'
        verbose_name_plural = '检测评级'
        ordering = ['rpn_score']

    def __str__(self):
        return f"{self.rating} - {self.name}"
    
    def save(self, *args, **kwargs):
        """保存时自动设置RPN分数"""
        if self.rating in self.RPN_SCORES:
            self.rpn_score = self.RPN_SCORES[self.rating]
        super().save(*args, **kwargs)


class FailureModeDetection(models.Model):
    """故障模式检测关联模型"""
    failure_mode = models.ForeignKey(
        'failure.FailureMode',
        on_delete=models.CASCADE,
        related_name='detections',
        verbose_name='故障模式'
    )
    detection_method = models.ForeignKey(
        DetectionMethod,
        on_delete=models.CASCADE,
        related_name='failure_modes',
        verbose_name='检测方法'
    )
    detection_rating = models.ForeignKey(
        DetectionRating,
        on_delete=models.CASCADE,
        related_name='failure_modes',
        verbose_name='检测评级'
    )
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
        db_table = 'failure_mode_detections'
        verbose_name = '故障模式检测'
        verbose_name_plural = '故障模式检测'
        unique_together = ('failure_mode', 'detection_method')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.failure_mode.name} - {self.detection_method.name}"