from django.db import models
from django.contrib.auth import get_user_model
from failure.models import FailureMode

User = get_user_model()


class SeverityLevel(models.Model):
    """严酷度等级定义模型"""
    LEVEL_CHOICES = [
        ('Ⅰ', 'Ⅰ级（灾难性）'),
        ('Ⅱ', 'Ⅱ级（严重）'),
        ('Ⅲ', 'Ⅲ级（中等）'),
        ('Ⅳ', 'Ⅳ级（轻微）'),
    ]
    
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        unique=True,
        verbose_name='严酷度等级'
    )
    name = models.CharField(max_length=50, verbose_name='等级名称')
    description = models.TextField(verbose_name='等级描述')
    criteria = models.TextField(verbose_name='评定标准')
    score = models.DecimalField(max_digits=5, decimal_places=2, unique=True, verbose_name='等级分数')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='创建人'
    )

    class Meta:
        db_table = 'severity_levels'
        verbose_name = '严酷度等级'
        verbose_name_plural = '严酷度等级'
        ordering = ['score']

    def __str__(self):
        return f"{self.level} - {self.name}"


class SeverityIndicator(models.Model):
    """严酷度指标配置模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='指标名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='指标编码')
    description = models.TextField(verbose_name='指标描述')
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name='指标权重')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='创建人'
    )

    class Meta:
        db_table = 'severity_indicators'
        verbose_name = '严酷度指标'
        verbose_name_plural = '严酷度指标'
        ordering = ['name']

    def __str__(self):
        return self.name


class SeverityAssessment(models.Model):
    """严酷度评定模型"""
    failure_mode = models.ForeignKey(
        FailureMode,
        on_delete=models.CASCADE,
        related_name='severity_assessments',
        verbose_name='故障模式'
    )
    severity_level = models.ForeignKey(
        SeverityLevel,
        on_delete=models.CASCADE,
        related_name='assessments',
        verbose_name='严酷度等级'
    )
    severity_value = models.IntegerField(default=1, verbose_name='严酷度S', help_text='范围1-10')
    occurrence_value = models.IntegerField(default=1, verbose_name='发生度O', help_text='范围1-10')
    detection_value = models.IntegerField(default=1, verbose_name='检测度D', help_text='范围1-10')
    rpn_value = models.IntegerField(default=1, verbose_name='风险优先数RPN', help_text='由S×O×D计算得出')
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='评定分数')
    project_instance_name = models.CharField(max_length=255, default='', verbose_name='项目实例名称')
    evaluation = models.TextField(blank=True, null=True, verbose_name='评定说明')
    evidence = models.TextField(blank=True, verbose_name='评定依据')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='创建人'
    )

    class Meta:
        db_table = 'severity_assessments'
        verbose_name = '严酷度评定'
        verbose_name_plural = '严酷度评定'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.failure_mode.name} - {self.severity_level.level}"
