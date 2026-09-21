from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Q
from auth_app.models import CustomUser, CustomRole, CustomPermission
from equipment.models import EquipmentType, EquipmentInstance
from failure.models import FailureMode, FailureCause, FailureEffect
from severity.models import SeverityLevel, SeverityIndicator, SeverityAssessment
from failure_analysis.models import HazardAnalysisParameter, FailureModeHazardAnalysis
from compensation.models import CompensationMeasure, EffectivenessEvaluation, FailureModeCompensation
from detection.models import DetectionMethod, DetectionRating, FailureModeDetection
from product_analysis.models import ProductHazardAnalysis

class Command(BaseCommand):
    help = '检查所有数据库表中的异常数据'

    def check_field(self, model, field_name, search_terms, model_name):
        """检查指定字段中是否包含异常字符"""
        query = Q()
        for term in search_terms:
            query |= Q(**{f"{field_name}__icontains": term})
        
        abnormal = model.objects.filter(query)
        if abnormal.exists():
            self.stdout.write(f"\n  {model_name}.{field_name}: 发现 {abnormal.count()} 条异常记录")
            for item in abnormal[:5]:  # 只显示前5条
                value = getattr(item, field_name)
                self.stdout.write(f"    ID: {item.id}, 值: {value[:100]}...")
            if abnormal.count() > 5:
                self.stdout.write(f"    ... 还有 {abnormal.count() - 5} 条记录")
            return abnormal.count()
        return 0

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("全面数据库异常数据检查")
        self.stdout.write("=" * 80)

        search_terms = ['弦', '约会', '智']
        total_abnormal = 0

        # 检查用户相关表
        self.stdout.write("\n【用户相关表】")
        total_abnormal += self.check_field(CustomUser, 'username', search_terms, 'CustomUser.username')
        total_abnormal += self.check_field(CustomUser, 'first_name', search_terms, 'CustomUser.first_name')
        total_abnormal += self.check_field(CustomUser, 'last_name', search_terms, 'CustomUser.last_name')
        total_abnormal += self.check_field(CustomUser, 'email', search_terms, 'CustomUser.email')
        
        total_abnormal += self.check_field(CustomRole, 'name', search_terms, 'CustomRole.name')
        total_abnormal += self.check_field(CustomRole, 'description', search_terms, 'CustomRole.description')
        
        total_abnormal += self.check_field(CustomPermission, 'name', search_terms, 'CustomPermission.name')
        total_abnormal += self.check_field(CustomPermission, 'description', search_terms, 'CustomPermission.description')

        # 检查设备管理表
        self.stdout.write("\n【设备管理表】")
        total_abnormal += self.check_field(EquipmentType, 'name', search_terms, 'EquipmentType.name')
        total_abnormal += self.check_field(EquipmentType, 'code', search_terms, 'EquipmentType.code')
        total_abnormal += self.check_field(EquipmentType, 'specifications', search_terms, 'EquipmentType.specifications')
        
        total_abnormal += self.check_field(EquipmentInstance, 'name', search_terms, 'EquipmentInstance.name')
        total_abnormal += self.check_field(EquipmentInstance, 'serial_number', search_terms, 'EquipmentInstance.serial_number')

        # 检查故障模式表
        self.stdout.write("\n【故障模式表】")
        total_abnormal += self.check_field(FailureMode, 'name', search_terms, 'FailureMode.name')
        total_abnormal += self.check_field(FailureMode, 'code', search_terms, 'FailureMode.code')
        total_abnormal += self.check_field(FailureMode, 'description', search_terms, 'FailureMode.description')
        
        total_abnormal += self.check_field(FailureCause, 'name', search_terms, 'FailureCause.name')
        total_abnormal += self.check_field(FailureCause, 'description', search_terms, 'FailureCause.description')
        
        total_abnormal += self.check_field(FailureEffect, 'name', search_terms, 'FailureEffect.name')
        total_abnormal += self.check_field(FailureEffect, 'description', search_terms, 'FailureEffect.description')

        # 检查严酷度管理表
        self.stdout.write("\n【严酷度管理表】")
        total_abnormal += self.check_field(SeverityLevel, 'name', search_terms, 'SeverityLevel.name')
        total_abnormal += self.check_field(SeverityLevel, 'description', search_terms, 'SeverityLevel.description')
        
        total_abnormal += self.check_field(SeverityIndicator, 'name', search_terms, 'SeverityIndicator.name')
        total_abnormal += self.check_field(SeverityIndicator, 'description', search_terms, 'SeverityIndicator.description')
        
        total_abnormal += self.check_field(SeverityAssessment, 'evaluation', search_terms, 'SeverityAssessment.evaluation')
        total_abnormal += self.check_field(SeverityAssessment, 'evidence', search_terms, 'SeverityAssessment.evidence')

        # 检查检测方法表
        self.stdout.write("\n【检测方法表】")
        total_abnormal += self.check_field(DetectionMethod, 'name', search_terms, 'DetectionMethod.name')
        total_abnormal += self.check_field(DetectionMethod, 'description', search_terms, 'DetectionMethod.description')
        
        total_abnormal += self.check_field(DetectionRating, 'name', search_terms, 'DetectionRating.name')
        total_abnormal += self.check_field(DetectionRating, 'description', search_terms, 'DetectionRating.description')

        # 检查补偿措施表
        self.stdout.write("\n【补偿措施表】")
        total_abnormal += self.check_field(CompensationMeasure, 'name', search_terms, 'CompensationMeasure.name')
        total_abnormal += self.check_field(CompensationMeasure, 'description', search_terms, 'CompensationMeasure.description')
        
        total_abnormal += self.check_field(EffectivenessEvaluation, 'notes', search_terms, 'EffectivenessEvaluation.notes')

        # 检查故障模式危害度分析表
        self.stdout.write("\n【故障模式危害度分析表】")
        total_abnormal += self.check_field(FailureModeHazardAnalysis, 'recommended_action', search_terms, 'FailureModeHazardAnalysis.recommended_action')
        total_abnormal += self.check_field(FailureModeHazardAnalysis, 'notes', search_terms, 'FailureModeHazardAnalysis.notes')
        
        total_abnormal += self.check_field(HazardAnalysisParameter, 'name', search_terms, 'HazardAnalysisParameter.name')
        total_abnormal += self.check_field(HazardAnalysisParameter, 'description', search_terms, 'HazardAnalysisParameter.description')

        # 检查产品危害度分析表
        self.stdout.write("\n【产品危害度分析表】")
        total_abnormal += self.check_field(ProductHazardAnalysis, 'assessment_conclusion', search_terms, 'ProductHazardAnalysis.assessment_conclusion')
        total_abnormal += self.check_field(ProductHazardAnalysis, 'recommendations', search_terms, 'ProductHazardAnalysis.recommendations')

        # 检查空值和异常值
        self.stdout.write("\n【空值和异常值检查】")
        
        # 检查必填字段的空值
        self.stdout.write("\n  检查必填字段的空值:")
        
        # 用户表
        empty_users = CustomUser.objects.filter(username='')
        if empty_users.exists():
            self.stdout.write(f"    CustomUser.username 为空: {empty_users.count()} 条")
            total_abnormal += empty_users.count()
        
        # 故障模式表
        empty_failure_modes = FailureMode.objects.filter(name='')
        if empty_failure_modes.exists():
            self.stdout.write(f"    FailureMode.name 为空: {empty_failure_modes.count()} 条")
            total_abnormal += empty_failure_modes.count()
        
        # 危害度分析表
        empty_analyses = FailureModeHazardAnalysis.objects.filter(failure_mode__isnull=True)
        if empty_analyses.exists():
            self.stdout.write(f"    FailureModeHazardAnalysis.failure_mode 为空: {empty_analyses.count()} 条")
            total_abnormal += empty_analyses.count()

        # 检查数值异常
        self.stdout.write("\n  检查数值异常:")
        
        # 检查概率值超出范围
        invalid_probability = FailureModeHazardAnalysis.objects.filter(
            occurrence_probability__lt=0
        ) | FailureModeHazardAnalysis.objects.filter(
            occurrence_probability__gt=100
        ) | FailureModeHazardAnalysis.objects.filter(
            detection_probability__lt=0
        ) | FailureModeHazardAnalysis.objects.filter(
            detection_probability__gt=100
        )
        
        if invalid_probability.exists():
            self.stdout.write(f"    概率值超出范围(0-100): {invalid_probability.count()} 条")
            for item in invalid_probability[:3]:
                self.stdout.write(f"      ID: {item.id}, 发生概率: {item.occurrence_probability}, 检测概率: {item.detection_probability}")
            total_abnormal += invalid_probability.count()

        # 检查严酷度值异常
        invalid_severity = FailureModeHazardAnalysis.objects.filter(
            severity_value__lt=0
        ) | FailureModeHazardAnalysis.objects.filter(
            severity_value__gt=100
        )
        
        if invalid_severity.exists():
            self.stdout.write(f"    严酷度值异常(应在0-100之间): {invalid_severity.count()} 条")
            for item in invalid_severity[:3]:
                self.stdout.write(f"      ID: {item.id}, 严酷度值: {item.severity_value}")
            total_abnormal += invalid_severity.count()

        # 检查RPN值异常
        invalid_rpn = FailureModeHazardAnalysis.objects.filter(
            risk_priority_number__lt=0
        ) | FailureModeHazardAnalysis.objects.filter(
            risk_priority_number__gt=1000
        )
        
        if invalid_rpn.exists():
            self.stdout.write(f"    RPN值异常(应在0-1000之间): {invalid_rpn.count()} 条")
            for item in invalid_rpn[:3]:
                self.stdout.write(f"      ID: {item.id}, RPN: {item.risk_priority_number}")
            total_abnormal += invalid_rpn.count()

        # 检查重复数据
        self.stdout.write("\n【重复数据检查】")
        
        # 检查重复的用户名
        duplicate_users = CustomUser.objects.values('username').annotate(
            count=models.Count('username')
        ).filter(count__gt=1)
        if duplicate_users.exists():
            self.stdout.write(f"    重复的用户名: {duplicate_users.count()} 个")
            for dup in duplicate_users:
                self.stdout.write(f"      用户名: {dup['username']}, 数量: {dup['count']}")
            total_abnormal += duplicate_users.count()

        # 检查重复的故障模式名称
        duplicate_failure_modes = FailureMode.objects.values('name').annotate(
            count=models.Count('name')
        ).filter(count__gt=1)
        if duplicate_failure_modes.exists():
            self.stdout.write(f"    重复的故障模式名称: {duplicate_failure_modes.count()} 个")
            for dup in duplicate_failure_modes[:3]:
                self.stdout.write(f"      名称: {dup['name']}, 数量: {dup['count']}")
            total_abnormal += duplicate_failure_modes.count()

        # 统计汇总
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("检查汇总")
        self.stdout.write("=" * 80)
        self.stdout.write(f"总异常记录数: {total_abnormal}")
        
        if total_abnormal == 0:
            self.stdout.write("\n✅ 数据库检查完成，未发现异常数据")
        else:
            self.stdout.write(f"\n⚠️  发现 {total_abnormal} 条异常数据，请及时处理")
            self.stdout.write("\n建议操作:")
            self.stdout.write("1. 检查并删除异常数据")
            self.stdout.write("2. 更新为正确的数据")
            self.stdout.write("3. 检查数据导入脚本")
            self.stdout.write("4. 检查前端示例数据")