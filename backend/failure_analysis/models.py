from django.db import models
from django.contrib.auth import get_user_model
from failure.models import FailureMode
from severity.models import SeverityLevel

User = get_user_model()


class HazardAnalysisParameter(models.Model):
    """危害度参数配置模型"""
    PARAMETER_TYPE_CHOICES = [
        ('severity', '严酷度'),
        ('occurrence', '发生概率'),
        ('detection', '检测概率'),
        ('risk', '风险优先级'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='参数名称')
    parameter_type = models.CharField(
        max_length=20,
        choices=PARAMETER_TYPE_CHOICES,
        verbose_name='参数类型'
    )
    description = models.TextField(blank=True, verbose_name='参数描述')
    min_value = models.FloatField(verbose_name='最小值')
    max_value = models.FloatField(verbose_name='最大值')
    default_value = models.FloatField(verbose_name='默认值')
    unit = models.CharField(max_length=20, blank=True, verbose_name='单位')
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
        db_table = 'hazard_analysis_parameters'
        verbose_name = '危害度参数'
        verbose_name_plural = '危害度参数'
        ordering = ['parameter_type', 'name']

    def __str__(self):
        return f"{self.name} ({self.parameter_type})"


class FailureModeHazardAnalysis(models.Model):
    """故障模式危害度分析模型"""
    RISK_LEVEL_CHOICES = [
        ('low', '低风险'),
        ('medium', '中等风险'),
        ('high', '高风险'),
        ('critical', '严重风险'),
    ]
    
    failure_mode = models.OneToOneField(
        FailureMode,
        on_delete=models.CASCADE,
        related_name='hazard_analysis',
        verbose_name='故障模式'
    )
    severity_level = models.ForeignKey(
        SeverityLevel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='hazard_analyses',
        verbose_name='严酷度等级'
    )
    severity_value = models.FloatField(verbose_name='严酷度值')
    occurrence_probability = models.FloatField(verbose_name='发生概率(%)')
    detection_probability = models.FloatField(verbose_name='检测概率(%)')
    risk_priority_number = models.FloatField(verbose_name='风险优先级数(RPN)')
    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        verbose_name='风险等级'
    )
    recommended_action = models.TextField(blank=True, verbose_name='使用补偿措施')
    analysis_date = models.DateField(auto_now_add=True, verbose_name='分析日期')
    notes = models.TextField(blank=True, verbose_name='分析说明')
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
        db_table = 'failure_mode_hazard_analyses'
        verbose_name = '故障模式危害度分析'
        verbose_name_plural = '故障模式危害度分析'
        ordering = ['-risk_priority_number', '-severity_value']

    def __str__(self):
        return f"{self.failure_mode.name} - 危害度分析"
    
    def calculate_rpn(self):
        """计算风险优先级数(RPN)"""
        # RPN = 严酷度值 × 发生概率 × 检测概率
        from decimal import Decimal
        severity = float(self.severity_value) if isinstance(self.severity_value, Decimal) else self.severity_value
        occurrence = float(self.occurrence_probability) if isinstance(self.occurrence_probability, Decimal) else self.occurrence_probability
        detection = float(self.detection_probability) if isinstance(self.detection_probability, Decimal) else self.detection_probability
        return severity * (occurrence / 100) * (detection / 100)
    
    def determine_risk_level(self):
        """根据RPN值确定风险等级"""
        if self.risk_priority_number >= 100:
            return 'critical'
        elif self.risk_priority_number >= 50:
            return 'high'
        elif self.risk_priority_number >= 20:
            return 'medium'
        else:
            return 'low'
    
    def save(self, *args, **kwargs):
        """保存前自动计算RPN和风险等级"""
        if not self.severity_level:
            # 如果没有指定严酷度等级，使用默认值
            try:
                self.severity_level = SeverityLevel.objects.get(level='Ⅲ')
                self.severity_value = self.severity_level.score
            except SeverityLevel.DoesNotExist:
                # 如果默认严酷度等级不存在，使用默认值
                self.severity_value = self.severity_value or 4.0
        else:
            # 使用严酷度等级的分数作为严酷度值
            self.severity_value = self.severity_level.score
        
        # 计算RPN
        self.risk_priority_number = self.calculate_rpn()
        
        # 确定风险等级
        self.risk_level = self.determine_risk_level()
        
        super().save(*args, **kwargs)
