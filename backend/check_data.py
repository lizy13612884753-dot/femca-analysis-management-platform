"""
检查产品危害度分析数据
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
django.setup()

from product_analysis.models import ProductHazardAnalysis
from failure_analysis.models import FailureModeHazardAnalysis

print("=" * 60)
print("产品危害度分析数据检查")
print("=" * 60)

for pa in ProductHazardAnalysis.objects.all():
    print(f"\n设备类型: {pa.equipment_type.name}")
    print(f"  总故障模式数: {pa.total_failure_modes}")
    print(f"  已分析故障模式数: {pa.analyzed_failure_modes}")
    
    # 获取该设备类型的故障模式危害度分析
    analyses = FailureModeHazardAnalysis.objects.filter(
        failure_mode__equipment_type=pa.equipment_type
    )
    
    print(f"  实际故障模式危害度分析数量: {analyses.count()}")
    print(f"  故障模式列表:")
    for analysis in analyses:
        print(f"    - {analysis.failure_mode.name}, RPN: {analysis.risk_priority_number}")
    
print("\n" + "=" * 60)