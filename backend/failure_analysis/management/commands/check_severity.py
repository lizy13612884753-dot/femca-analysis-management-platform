from django.core.management.base import BaseCommand
from failure_analysis.models import FailureModeHazardAnalysis

class Command(BaseCommand):
    help = '查看严酷度值异常的数据'

    def handle(self, *args, **options):
        self.stdout.write("严酷度值异常的数据:")
        analyses = FailureModeHazardAnalysis.objects.filter(severity_value__gt=10)
        
        for analysis in analyses:
            self.stdout.write(f"ID: {analysis.id}")
            self.stdout.write(f"  严酷度值: {analysis.severity_value}")
            self.stdout.write(f"  故障模式: {analysis.failure_mode}")
            self.stdout.write(f"  严酷度等级: {analysis.severity_level}")
            self.stdout.write(f"  发生概率: {analysis.occurrence_probability}")
            self.stdout.write(f"  检测概率: {analysis.detection_probability}")
            self.stdout.write(f"  RPN: {analysis.risk_priority_number}")
            self.stdout.write(f"  风险等级: {analysis.risk_level}")
            self.stdout.write("-" * 50)