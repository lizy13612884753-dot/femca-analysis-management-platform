from django.core.management.base import BaseCommand
from severity.models import SeverityLevel

class Command(BaseCommand):
    help = '查看严酷度等级的分数设置'

    def handle(self, *args, **options):
        self.stdout.write("严酷度等级分数设置:")
        levels = SeverityLevel.objects.all().order_by('score')
        
        for level in levels:
            self.stdout.write(f"等级: {level.level}")
            self.stdout.write(f"  名称: {level.name}")
            self.stdout.write(f"  分数: {level.score}")
            self.stdout.write(f"  描述: {level.description}")
            self.stdout.write("-" * 50)