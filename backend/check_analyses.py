from failure_analysis.models import FailureModeHazardAnalysis
from failure.models import FailureMode

print("=== 故障模式危害度分析数据 ===")
analyses = FailureModeHazardAnalysis.objects.all()
print(f"总记录数: {analyses.count()}")

print("\n=== 所有记录详情 ===")
for analysis in analyses:
    print(f"\nID: {analysis.id}")
    print(f"故障模式: {analysis.failure_mode}")
    print(f"严酷度值: {analysis.severity_value}")
    print(f"发生概率: {analysis.occurrence_probability}")
    print(f"检测概率: {analysis.detection_probability}")
    print(f"风险优先级数: {analysis.risk_priority_number}")
    print(f"风险等级: {analysis.risk_level}")
    print(f"使用补偿措施: {analysis.recommended_action}")
    print(f"分析说明: {analysis.notes}")
    print(f"创建人: {analysis.created_by}")
    print(f"创建时间: {analysis.created_at}")
    print("-" * 50)

print("\n=== 检查异常数据 ===")
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
    print(f"\n发现 {abnormal_data.count()} 条异常记录:")
    for data in abnormal_data:
        print(f"ID: {data.id}, 补偿措施: {data.recommended_action}, 说明: {data.notes}")
else:
    print("\n未发现异常记录")