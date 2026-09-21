from django.db import models
from django.contrib.auth import get_user_model
from equipment.models import EquipmentType
from failure_analysis.models import FailureModeHazardAnalysis

User = get_user_model()


class ProductHazardAnalysis(models.Model):
    """产品危害度分析模型"""
    RISK_LEVEL_CHOICES = [
        ('low', '低风险'),
        ('medium', '中等风险'),
        ('high', '高风险'),
        ('critical', '严重风险'),
    ]
    
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='hazard_analyses',
        verbose_name='设备类型'
    )
    analysis_date = models.DateField(auto_now_add=True, verbose_name='分析日期')
    
    # 汇总统计数据
    total_failure_modes = models.PositiveIntegerField(default=0, verbose_name='总故障模式数')
    analyzed_failure_modes = models.PositiveIntegerField(default=0, verbose_name='已分析故障模式数')
    
    # 危害度汇总值
    avg_severity = models.FloatField(default=0, verbose_name='平均严酷度')
    avg_occurrence = models.FloatField(default=0, verbose_name='平均发生概率(%)')
    avg_detection = models.FloatField(default=0, verbose_name='平均检测概率(%)')
    avg_rpn = models.FloatField(default=0, verbose_name='平均风险优先级数(RPN)')
    max_rpn = models.FloatField(default=0, verbose_name='最高RPN值')
    min_rpn = models.FloatField(default=0, verbose_name='最低RPN值')
    
    # 风险等级分布
    critical_count = models.PositiveIntegerField(default=0, verbose_name='严重风险数')
    high_count = models.PositiveIntegerField(default=0, verbose_name='高风险数')
    medium_count = models.PositiveIntegerField(default=0, verbose_name='中等风险数')
    low_count = models.PositiveIntegerField(default=0, verbose_name='低风险数')
    
    # 整体风险评估
    overall_risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVEL_CHOICES,
        default='low',
        verbose_name='整体风险等级'
    )
    assessment_conclusion = models.TextField(blank=True, verbose_name='评估结论')
    recommendations = models.TextField(blank=True, verbose_name='改进建议')
    
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
        db_table = 'product_hazard_analyses'
        verbose_name = '产品危害度分析'
        verbose_name_plural = '产品危害度分析'
        ordering = ['-analysis_date']

    def __str__(self):
        return f"{self.equipment_type.name} - 危害度分析 ({self.analysis_date})"
    
    def calculate_overall_risk_level(self):
        """根据风险分布确定整体风险等级"""
        if self.critical_count > 0:
            return 'critical'
        elif self.high_count > (self.analyzed_failure_modes * 0.3):  # 超过30%为高风险
            return 'high'
        elif self.medium_count > (self.analyzed_failure_modes * 0.5):  # 超过50%为中等风险
            return 'medium'
        else:
            return 'low'
    
    def update_analysis_data(self):
        """更新分析数据（汇总所有故障模式的危害度分析）"""
        # 获取该设备类型下所有故障模式的危害度分析
        failure_analyses = FailureModeHazardAnalysis.objects.filter(
            failure_mode__equipment_type=self.equipment_type,
            is_active=True
        ).select_related('failure_mode')
        
        # 获取该设备类型下所有故障模式数（只计算启用的故障模式）
        self.total_failure_modes = self.equipment_type.failure_modes.filter(is_active=True).count()
        self.analyzed_failure_modes = failure_analyses.count()
        
        if self.analyzed_failure_modes > 0:
            # 计算平均值
            total_severity = 0
            total_occurrence = 0
            total_detection = 0
            total_rpn = 0
            rpn_values = []
            
            # 风险等级计数
            risk_counts = {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
            
            for analysis in failure_analyses:
                total_severity += analysis.severity_value
                total_occurrence += analysis.occurrence_probability
                total_detection += analysis.detection_probability
                total_rpn += analysis.risk_priority_number
                rpn_values.append(analysis.risk_priority_number)
                risk_counts[analysis.risk_level] += 1
            
            # 设置汇总值
            self.avg_severity = total_severity / self.analyzed_failure_modes
            self.avg_occurrence = total_occurrence / self.analyzed_failure_modes
            self.avg_detection = total_detection / self.analyzed_failure_modes
            self.avg_rpn = total_rpn / self.analyzed_failure_modes
            self.max_rpn = max(rpn_values)
            self.min_rpn = min(rpn_values)
            
            # 设置风险等级分布
            self.critical_count = risk_counts['critical']
            self.high_count = risk_counts['high']
            self.medium_count = risk_counts['medium']
            self.low_count = risk_counts['low']
        
        # 确定整体风险等级
        self.overall_risk_level = self.calculate_overall_risk_level()
        
        # 保存更新
        self.save()
