#!/usr/bin/env python3
"""
检查数据库中设备实例的功能描述字段数据
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
import django
django.setup()

from equipment.models import EquipmentInstance


def check_function_description_data():
    """检查数据库中设备实例的功能描述字段数据"""
    print("检查数据库中的功能描述字段数据...\n")
    
    # 获取所有设备实例
    instances = EquipmentInstance.objects.all()
    print(f"设备实例总数: {instances.count()}\n")
    
    # 遍历所有设备实例
    for i, instance in enumerate(instances, 1):
        print(f"设备实例 {i}: ID = {instance.id}")
        print(f"  名称: {instance.name}")
        print(f"  功能描述: '{instance.function_description}'")
        print(f"  功能描述长度: {len(instance.function_description) if instance.function_description else 0}")
        print(f"  功能描述类型: {type(instance.function_description)}")
        print(f"  是否为空: {not instance.function_description}")
        print()


if __name__ == "__main__":
    check_function_description_data()