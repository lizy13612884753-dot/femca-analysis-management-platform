from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CompensationMeasure(models.Model):
    """补偿措施模型"""
    MEASURE_TYPE_CHOICES = [
        ('preventive', '预防性'),
        ('corrective', '纠正性'),
        ('detection', '检测性'),
        ('mitigation', '缓解性'),
        ('redundancy', '冗余性'),
        ('other', '其他'),
    ]
    
    COMPLEXITY_CHOICES = [
        ('simple', '简单'),
        ('moderate', '中等'),
        ('complex', '复杂'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name='补偿措施名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='补偿措施编码')
    description = models.TextField(blank=True, verbose_name='补偿措施描述')
    measure_type = models.CharField(
        max_length=20, 
        choices=MEASURE_TYPE_CHOICES, 
        default='corrective', 
        verbose_name='措施类型'
    )
    equipment_types = models.ManyToManyField(
        'equipment.EquipmentType',
        blank=True,
        verbose_name='适用设备类型'
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='成本')
    time_required = models.PositiveIntegerField(default=0, verbose_name='所需时间（分钟）')
    effectiveness = models.FloatField(default=0.8, verbose_name='预期效果（0-1）')
    implementation_complexity = models.CharField(
        max_length=20, 
        choices=COMPLEXITY_CHOICES, 
        default='moderate', 
        verbose_name='实施复杂性'
    )
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
        db_table = 'compensation_measures'
        verbose_name = '补偿措施'
        verbose_name_plural = '补偿措施'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_measure_type_display_name(self):
        """获取措施类型显示名称"""
        return dict(self.MEASURE_TYPE_CHOICES).get(self.measure_type, self.measure_type)
    
    def get_complexity_display_name(self):
        """获取复杂性显示名称"""
        return dict(self.COMPLEXITY_CHOICES).get(self.implementation_complexity, self.implementation_complexity)


class EffectivenessEvaluation(models.Model):
    """有效性评估模型"""
    compensation_measure = models.ForeignKey(
        CompensationMeasure,
        on_delete=models.CASCADE,
        related_name='effectiveness_evaluations',
        verbose_name='补偿措施'
    )
    evaluation_date = models.DateField(verbose_name='评估日期')
    evaluator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='评估人'
    )
    actual_effectiveness = models.FloatField(default=0.8, verbose_name='实际效果（0-1）')
    notes = models.TextField(blank=True, verbose_name='评估备注')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'effectiveness_evaluations'
        verbose_name = '有效性评估'
        verbose_name_plural = '有效性评估'
        ordering = ['-evaluation_date']

    def __str__(self):
        return f"{self.compensation_measure.name} - {self.evaluation_date}"


class FailureModeCompensation(models.Model):
    """故障模式补偿关联模型"""
    RATING_CHOICES = [
        ('A', 'A - 优秀'),
        ('B', 'B - 良好'),
        ('C', 'C - 一般'),
        ('D', 'D - 较差'),
        ('E', 'E - 差'),
        ('F', 'F - 很差'),
        ('G', 'G - 无效'),
    ]
    
    failure_mode = models.ForeignKey(
        'failure.FailureMode',
        on_delete=models.CASCADE,
        related_name='compensations',
        verbose_name='故障模式'
    )
    compensation_measure = models.ForeignKey(
        CompensationMeasure,
        on_delete=models.CASCADE,
        related_name='failure_modes',
        verbose_name='补偿措施'
    )
    effectiveness_rating = models.CharField(
        max_length=1, 
        choices=RATING_CHOICES, 
        default='C', 
        verbose_name='效果评级'
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
        db_table = 'failure_mode_compensations'
        verbose_name = '故障模式补偿'
        verbose_name_plural = '故障模式补偿'
        unique_together = ('failure_mode', 'compensation_measure')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.failure_mode.name} - {self.compensation_measure.name}"
    
    def get_rating_display_name(self):
        """获取评级显示名称"""
        return dict(self.RATING_CHOICES).get(self.effectiveness_rating, self.effectiveness_rating)