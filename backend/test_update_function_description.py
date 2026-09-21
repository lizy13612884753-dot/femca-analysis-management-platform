#!/usr/bin/env python3
"""
测试直接更新设备实例的功能描述字段
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


def test_update_function_description():
    """测试更新设备实例的功能描述字段"""
    print("开始测试更新功能描述字段...")
    
    # 获取第一个设备实例
    instance = EquipmentInstance.objects.first()
    if not instance:
        print("没有找到设备实例，创建一个新的...")
        from django.contrib.auth.models import User
        # 获取第一个用户作为创建人
        user = User.objects.first()
        if not user:
            print("没有找到用户，无法创建设备实例")
            return
        
        # 创建一个新的设备实例
        from equipment.models import EquipmentType
        equipment_type = EquipmentType.objects.first()
        if not equipment_type:
            print("没有找到设备类型，无法创建设备实例")
            return
        
        instance = EquipmentInstance.objects.create(
            name="测试设备",
            serial_number="TEST001",
            equipment_type=equipment_type,
            created_by=user
        )
        print(f"创建了新设备实例: {instance.name} (ID: {instance.id})")
    
    print(f"\n原始数据:")
    print(f"设备实例: {instance.name} (ID: {instance.id})")
    print(f"功能描述: '{instance.function_description}'")
    
    # 更新功能描述
    new_description = "这是一个测试功能描述"
    print(f"\n更新功能描述为: '{new_description}'")
    
    instance.function_description = new_description
    instance.save()
    
    # 重新获取实例，确保数据已保存
    updated_instance = EquipmentInstance.objects.get(id=instance.id)
    print(f"\n更新后的数据:")
    print(f"功能描述: '{updated_instance.function_description}'")
    
    if updated_instance.function_description == new_description:
        print("✓ 功能描述更新成功！")
    else:
        print("✗ 功能描述更新失败！")
    
    print(f"\n测试完成。")


if __name__ == "__main__":
    test_update_function_description()