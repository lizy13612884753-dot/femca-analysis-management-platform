"""
完整初始化数据库的脚本
创建设备类型、故障模式、检测方法、补偿措施等基础数据
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from equipment.models import EquipmentType
from failure.models import FailureMode, FailureCause, FailureEffect
from detection.models import DetectionMethod, DetectionRating
from compensation.models import CompensationMeasure
from severity.models import SeverityLevel

User = get_user_model()

def create_admin_user():
    """创建管理员用户"""
    try:
        user = User.objects.get(username='admin')
        print("✓ admin用户已存在")
        return user
    except User.DoesNotExist:
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✓ 创建了admin用户")
        return user

def create_equipment_types(user):
    """创建设备类型"""
    equipment_types_data = [
        {
            'name': '液压系统',
            'code': 'HYDRAULIC',
            'description': '液压传动系统，包括液压泵、液压阀等',
            'category': '动力系统',
            'manufacturer': '博世力士乐',
            'status': 'active',
            'created_by': user
        },
        {
            'name': '电气系统',
            'code': 'ELECTRICAL',
            'description': '电气控制系统，包括电机、控制器等',
            'category': '控制系统',
            'manufacturer': '西门子',
            'status': 'active',
            'created_by': user
        },
        {
            'name': '机械传动系统',
            'code': 'MECHANICAL',
            'description': '机械传动系统，包括齿轮箱、联轴器等',
            'category': '传动系统',
            'manufacturer': 'SEW',
            'status': 'active',
            'created_by': user
        },
        {
            'name': '制动系统',
            'code': 'BRAKING',
            'description': '制动系统，包括制动器、制动阀等',
            'category': '安全系统',
            'manufacturer': '克诺尔',
            'status': 'active',
            'created_by': user
        }
    ]
    
    created_count = 0
    for et_data in equipment_types_data:
        et, created = EquipmentType.objects.get_or_create(
            code=et_data['code'],
            defaults=et_data
        )
        if created:
            print(f"✓ 创建设备类型: {et.name}")
            created_count += 1
    
    print(f"设备类型初始化完成，共创建 {created_count} 条记录")
    return EquipmentType.objects.all()

def create_failure_modes(user, equipment_types):
    """创建故障模式"""
    failure_modes_data = [
        {
            'name': '制动力矩过小',
            'code': 'BRAKING_TORQUE_LOW',
            'description': '制动系统提供的制动力矩不足，无法有效制动',
            'equipment_type': equipment_types[3],
            'function_name': '制动功能',
            'function_status': '2',
            'failure_effect': '制动距离延长，安全隐患',
            'severity': 'A',
            'occurrence_rate': 30,
            'frequency': '偶尔发生',
            'causes': '制动器磨损、液压压力不足',
            'detection_methods': '制动力测试、目视检查',
            'created_by': user
        },
        {
            'name': '液压泄漏',
            'code': 'HYDRAULIC_LEAK',
            'description': '液压系统出现泄漏现象',
            'equipment_type': equipment_types[0],
            'function_name': '液压传动',
            'function_status': '2',
            'failure_effect': '系统压力下降，功能失效',
            'severity': 'B',
            'occurrence_rate': 25,
            'frequency': '较少发生',
            'causes': '密封件老化、管路破损',
            'detection_methods': '压力表检查、目视检查',
            'created_by': user
        },
        {
            'name': '电机过热',
            'code': 'MOTOR_OVERHEAT',
            'description': '电机运行温度过高',
            'equipment_type': equipment_types[1],
            'function_name': '电机驱动',
            'function_status': '2',
            'failure_effect': '电机损坏、寿命缩短',
            'severity': 'B',
            'occurrence_rate': 20,
            'frequency': '很少发生',
            'causes': '散热不良、负载过大',
            'detection_methods': '温度监测、仪器检测',
            'created_by': user
        },
        {
            'name': '齿轮磨损',
            'code': 'GEAR_WEAR',
            'description': '齿轮传动系统齿轮磨损严重',
            'equipment_type': equipment_types[2],
            'function_name': '机械传动',
            'function_status': '2',
            'failure_effect': '传动效率下降、噪音增大',
            'severity': 'C',
            'occurrence_rate': 40,
            'frequency': '经常发生',
            'causes': '润滑不良、负载过大',
            'detection_methods': '噪音检测、定期检查',
            'created_by': user
        },
        {
            'name': '控制系统故障',
            'code': 'CONTROL_FAILURE',
            'description': '电气控制系统出现故障',
            'equipment_type': equipment_types[1],
            'function_name': '系统控制',
            'function_status': '1',
            'failure_effect': '系统失控、停机',
            'severity': 'A',
            'occurrence_rate': 15,
            'frequency': '极少发生',
            'causes': '元器件老化、电磁干扰',
            'detection_methods': '自诊断、功能测试',
            'created_by': user
        },
        {
            'name': '压力异常',
            'code': 'PRESSURE_ABNORMAL',
            'description': '液压系统压力异常',
            'equipment_type': equipment_types[0],
            'function_name': '压力控制',
            'function_status': '2',
            'failure_effect': '系统性能下降',
            'severity': 'C',
            'occurrence_rate': 35,
            'frequency': '经常发生',
            'causes': '压力阀故障、泵损坏',
            'detection_methods': '压力表监测、性能测试',
            'created_by': user
        }
    ]
    
    created_count = 0
    for fm_data in failure_modes_data:
        fm, created = FailureMode.objects.get_or_create(
            code=fm_data['code'],
            defaults=fm_data
        )
        if created:
            print(f"✓ 创建故障模式: {fm.name}")
            created_count += 1
    
    print(f"故障模式初始化完成，共创建 {created_count} 条记录")
    return FailureMode.objects.all()

def create_detection_methods(user):
    """创建检测方法"""
    detection_methods_data = [
        {
            'name': '目视检查',
            'code': 'VISUAL',
            'description': '通过肉眼观察设备状态',
            'created_by': user
        },
        {
            'name': '仪器检测',
            'code': 'INSTRUMENT',
            'description': '使用专业仪器进行检测',
            'created_by': user
        },
        {
            'name': '性能测试',
            'code': 'PERFORMANCE',
            'description': '通过性能测试进行检测',
            'created_by': user
        },
        {
            'name': '定期维护检查',
            'code': 'MAINTENANCE',
            'description': '在定期维护时进行检查',
            'created_by': user
        }
    ]
    
    created_count = 0
    for dm_data in detection_methods_data:
        dm, created = DetectionMethod.objects.get_or_create(
            code=dm_data['code'],
            defaults=dm_data
        )
        if created:
            print(f"✓ 创建检测方法: {dm.name}")
            created_count += 1
    
    print(f"检测方法初始化完成，共创建 {created_count} 条记录")

def create_compensation_measures(user):
    """创建补偿措施"""
    compensation_measures_data = [
        {
            'name': '定期维护',
            'code': 'MAINTENANCE',
            'description': '建立定期维护计划，预防故障发生',
            'measure_type': 'preventive',
            'effectiveness': 0.9,
            'created_by': user
        },
        {
            'name': '冗余设计',
            'code': 'REDUNDANCY',
            'description': '采用冗余设计，提高系统可靠性',
            'measure_type': 'redundancy',
            'effectiveness': 0.95,
            'created_by': user
        },
        {
            'name': '早期预警',
            'code': 'EARLY_WARNING',
            'description': '建立早期预警系统，及时发现异常',
            'measure_type': 'detection',
            'effectiveness': 0.7,
            'created_by': user
        },
        {
            'name': '快速更换',
            'code': 'QUICK_REPLACE',
            'description': '准备备件，故障时快速更换',
            'measure_type': 'corrective',
            'effectiveness': 0.85,
            'created_by': user
        }
    ]
    
    created_count = 0
    for cm_data in compensation_measures_data:
        cm, created = CompensationMeasure.objects.get_or_create(
            code=cm_data['code'],
            defaults=cm_data
        )
        if created:
            print(f"✓ 创建补偿措施: {cm.name}")
            created_count += 1
    
    print(f"补偿措施初始化完成，共创建 {created_count} 条记录")

def main():
    print("=" * 60)
    print("开始初始化数据库")
    print("=" * 60)
    
    user = create_admin_user()
    
    equipment_types = create_equipment_types(user)
    failure_modes = create_failure_modes(user, equipment_types)
    create_detection_methods(user)
    create_compensation_measures(user)
    
    print("\n" + "=" * 60)
    print("数据库初始化完成！")
    print("=" * 60)
    print("\n可以使用以下命令运行后续脚本：")
    print("  python create_severity_levels.py  # 创建严酷度等级")
    print("  python create_test_data.py        # 创建测试数据")
    print("\n或访问 http://localhost:8000/admin/ 使用管理后台")

if __name__ == '__main__':
    main()
