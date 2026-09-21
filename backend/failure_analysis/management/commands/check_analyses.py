from django.core.management.base import BaseCommand
from failure_analysis.models import FailureModeHazardAnalysis

class Command(BaseCommand):
    help = '检查故障模式危害度分析数据'

    def handle(self, *args, **options):
        self.stdout.write("=== 故障模式危害度分析数据 ===")
        analyses = FailureModeHazardAnalysis.objects.all()
        self.stdout.write(f"总记录数: {analyses.count()}")

        self.stdout.write("\n=== 所有记录详情 ===")
        for analysis in analyses:
            self.stdout.write(f"\nID: {analysis.id}")
            self.stdout.write(f"故障模式: {analysis.failure_mode}")
            self.stdout.write(f"严酷度值: {analysis.severity_value}")
            self.stdout.write(f"发生概率: {analysis.occurrence_probability}")
            self.stdout.write(f"检测概率: {analysis.detection_probability}")
            self.stdout.write(f"风险优先级数: {analysis.risk_priority_number}")
            self.stdout.write(f"风险等级: {analysis.risk_level}")
            self.stdout.write(f"使用补偿措施: {analysis.recommended_action}")
            self.stdout.write(f"分析说明: {analysis.notes}")
            self.stdout.write(f"创建人: {analysis.created_by}")
            self.stdout.write(f"创建时间: {analysis.created_at}")
            self.stdout.write("-" * 50)

        self.stdout.write("\n=== 检查异常数据 ===")
        abnormal_data = analyses.filter(
            recommended_action__icontains='弦'
        ) | analyses.filter(
            recommended_action__icontains='约会'
        ) | analyses.filter(
            recommended_action__icontains='智'
        ) | analyses.filter(
            notes__icontains='弦'
        ) | analyses.filter(
            notes__icontains='约会'
        ) | analyses.filter(
            notes__icontains='智'
        )

        if abnormal_data.exists():
            self.stdout.write(f"\n发现 {abnormal_data.count()} 条异常记录:")
            for data in abnormal_data:
                self.stdout.write(f"ID: {data.id}, 补偿措施: {data.recommended_action}, 说明: {data.notes}")
        else:
            self.stdout.write("\n未发现异常记录")