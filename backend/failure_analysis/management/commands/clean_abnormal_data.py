from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Q
from auth_app.models import CustomUser
from failure.models import FailureMode
from failure_analysis.models import FailureModeHazardAnalysis

class Command(BaseCommand):
    help = '清理数据库中的异常数据'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write("开始清理异常数据")
        self.stdout.write("=" * 80)

        total_cleaned = 0

        # 1. 清理数值异常的危害度分析数据
        self.stdout.write("\n【1. 清理数值异常的危害度分析数据】")
        
        # 清理概率值超出范围的数据
        invalid_probability = FailureModeHazardAnalysis.objects.filter(
            occurrence_probability__gt=100
        ) | FailureModeHazardAnalysis.objects.filter(
            detection_probability__gt=100
        )
        
        if invalid_probability.exists():
            count = invalid_probability.count()
            self.stdout.write(f"  发现 {count} 条概率值超出范围的数据")
            for analysis in invalid_probability:
                # 将超出范围的值调整为最大值100
                if analysis.occurrence_probability > 100:
                    analysis.occurrence_probability = 100
                if analysis.detection_probability > 100:
                    analysis.detection_probability = 100
                analysis.save()
                total_cleaned += 1
            self.stdout.write(f"  ✓ 已修复 {count} 条概率值异常数据")
        
        # 清理严酷度值异常的数据
        invalid_severity = FailureModeHazardAnalysis.objects.filter(
            severity_value__gt=100
        )
        
        if invalid_severity.exists():
            count = invalid_severity.count()
            self.stdout.write(f"  发现 {count} 条严酷度值异常的数据")
            for analysis in invalid_severity:
                # 将超出范围的值调整为最大值100
                if analysis.severity_value > 100:
                    analysis.severity_value = 100
                analysis.save()
                total_cleaned += 1
            self.stdout.write(f"  ✓ 已修复 {count} 条严酷度值异常数据")

        # 2. 清理测试数据
        self.stdout.write("\n【2. 清理测试数据】")
        
        # 清理包含"测试"的备注
        test_notes = FailureModeHazardAnalysis.objects.filter(
            notes__icontains='测试'
        )
        
        if test_notes.exists():
            count = test_notes.count()
            self.stdout.write(f"  发现 {count} 条包含'测试'的备注")
            for analysis in test_notes:
                analysis.notes = ''
                analysis.save()
                total_cleaned += 1
            self.stdout.write(f"  ✓ 已清理 {count} 条测试备注")

        # 3. 处理重复的故障模式
        self.stdout.write("\n【3. 处理重复的故障模式】")
        
        # 查找重复的故障模式名称
        duplicate_failure_modes = FailureMode.objects.values('name').annotate(
            count=models.Count('name')
        ).filter(count__gt=1)
        
        if duplicate_failure_modes.exists():
            self.stdout.write(f"  发现 {duplicate_failure_modes.count()} 个重复的故障模式名称")
            for dup in duplicate_failure_modes:
                name = dup['name']
                count = dup['count']
                self.stdout.write(f"    故障模式: {name}, 数量: {count}")
                
                # 获取所有重复的故障模式
                modes = FailureMode.objects.filter(name=name).order_by('id')
                
                # 保留第一个，删除其他的
                for mode in modes[1:]:
                    self.stdout.write(f"      删除重复故障模式: ID={mode.id}, {mode.name}")
                    mode.delete()
                    total_cleaned += 1
            self.stdout.write(f"  ✓ 已清理重复故障模式")

        # 4. 重新计算RPN和风险等级
        self.stdout.write("\n【4. 重新计算RPN和风险等级】")
        
        analyses = FailureModeHazardAnalysis.objects.all()
        self.stdout.write(f"  重新计算 {analyses.count()} 条危害度分析数据")
        
        for analysis in analyses:
            # 重新计算RPN
            analysis.risk_priority_number = (
                analysis.severity_value * 
                analysis.occurrence_probability * 
                analysis.detection_probability
            ) / 10000  # 归一化到0-100范围
            
            # 重新确定风险等级
            rpn = analysis.risk_priority_number
            if rpn >= 50:
                analysis.risk_level = 'critical'
            elif rpn >= 30:
                analysis.risk_level = 'high'
            elif rpn >= 15:
                analysis.risk_level = 'medium'
            else:
                analysis.risk_level = 'low'
            
            analysis.save()
        
        self.stdout.write(f"  ✓ 已重新计算所有RPN和风险等级")

        # 5. 清理用户表中的测试数据
        self.stdout.write("\n【5. 清理用户表中的测试数据】")
        
        test_users = CustomUser.objects.filter(
            Q(username__icontains='test') |
            Q(email__icontains='test')
        ).exclude(username='admin')
        
        if test_users.exists():
            count = test_users.count()
            self.stdout.write(f"  发现 {count} 个测试用户")
            for user in test_users:
                self.stdout.write(f"    删除测试用户: {user.username}")
                user.delete()
                total_cleaned += 1
            self.stdout.write(f"  ✓ 已清理测试用户")

        # 汇总
        self.stdout.write("\n" + "=" * 80)
        self.stdout.write("清理完成")
        self.stdout.write("=" * 80)
        self.stdout.write(f"总共清理/修复了 {total_cleaned} 条数据")
        self.stdout.write("\n建议:")
        self.stdout.write("1. 检查清理后的数据是否正确")
        self.stdout.write("2. 运行 python manage.py check_all_abnormal_data 再次检查")
        self.stdout.write("3. 如有需要，重新导入正确的数据")