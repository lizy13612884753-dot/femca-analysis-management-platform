from failure.models import FailureMode
from failure_analysis.models import FailureModeHazardAnalysis

print('故障模式列表:')
for fm in FailureMode.objects.all():
    print(f'  - {fm.name} (ID: {fm.id}, 设备类型: {fm.equipment_type.name})')

print('\n故障模式危害度分析列表:')
for fma in FailureModeHazardAnalysis.objects.all():
    print(f'  - {fma.failure_mode.name} (RPN: {fma.risk_priority_number}, 风险等级: {fma.risk_level})')
