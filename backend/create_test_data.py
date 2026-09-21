"""
创建测试数据的脚本
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
django.setup()

from equipment.models import EquipmentType
from failure.models import FailureMode
from failure_analysis.models import FailureModeHazardAnalysis
from product_analysis.models import ProductHazardAnalysis
from severity.models import SeverityLevel
from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_data():
    print("开始创建测试数据...")
    
    # 获取或创建用户
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("创建了admin用户")
    
    # 获取设备类型
    equipment_types = EquipmentType.objects.all()
    if not equipment_types.exists():
        print("没有设备类型，请先创建设备类型")
        return
    
    # 获取故障模式
    failure_modes = FailureMode.objects.all()
    if not failure_modes.exists():
        print("没有故障模式，请先创建故障模式")
        return
    
    # 获取或创建严酷度等级
    severity_levels = SeverityLevel.objects.all()
    if not severity_levels.exists():
        print("没有严酷度等级，请先创建严酷度等级")
        return
    
    # 为每个故障模式创建危害度分析
    for i, failure_mode in enumerate(failure_modes):
        if FailureModeHazardAnalysis.objects.filter(failure_mode=failure_mode).exists():
            print(f"故障模式 {failure_mode.name} 已有危害度分析，跳过")
            continue
        
        # 随机选择严酷度等级
        severity_level = severity_levels[i % len(severity_levels)]
        
        # 创建危害度分析
        analysis = FailureModeHazardAnalysis.objects.create(
            failure_mode=failure_mode,
            severity_level=severity_level,
            severity_value=float(severity_level.score),
            occurrence_probability=float(50 + (i * 10)),
            detection_probability=float(50 + (i * 10)),
            notes=f'自动生成的测试数据 - {failure_mode.name}',
            created_by=user
        )
        
        print(f"创建了故障模式危害度分析: {failure_mode.name}, RPN: {analysis.risk_priority_number}")
    
    # 为每个设备类型创建产品危害度分析
    for equipment_type in equipment_types:
        if ProductHazardAnalysis.objects.filter(equipment_type=equipment_type).exists():
            print(f"设备类型 {equipment_type.name} 已有产品危害度分析，跳过")
            continue
        
        # 获取该设备类型的故障模式危害度分析
        hazard_analyses = FailureModeHazardAnalysis.objects.filter(
            failure_mode__equipment_type=equipment_type
        )
        
        if not hazard_analyses.exists():
            print(f"设备类型 {equipment_type.name} 没有故障模式危害度分析，跳过")
            continue
        
        # 创建产品危害度分析
        product_analysis = ProductHazardAnalysis.objects.create(
            equipment_type=equipment_type,
            assessment_conclusion=f'{equipment_type.name}的整体风险水平可控，建议定期维护。',
            recommendations=f'建议加强{equipment_type.name}的预防性维护，降低故障发生率。',
            created_by=user
        )
        
        # 更新分析数据
        product_analysis.update_analysis_data()
        
        print(f"创建了产品危害度分析: {equipment_type.name}, 平均RPN: {product_analysis.avg_rpn}")
    
    print("\n测试数据创建完成！")

if __name__ == '__main__':
    create_test_data()