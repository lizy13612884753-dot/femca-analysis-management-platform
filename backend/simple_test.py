#!/usr/bin/env python3
"""
最简单的测试脚本，直接测试序列化器
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
import django
django.setup()

# 直接导入模型和序列化器
from equipment.models import EquipmentInstance
from equipment.serializers import EquipmentInstanceSerializer

# 获取一个设备实例
instance = EquipmentInstance.objects.first()

if instance:
    print(f"设备实例: {instance.name}, ID: {instance.id}")
    print(f"功能描述: '{instance.function_description}'")
    
    # 创建序列化器
    serializer = EquipmentInstanceSerializer(instance)
    
    # 获取序列化后的数据
    serialized_data = serializer.data
    
    print(f"\n序列化后的数据字段: {sorted(serialized_data.keys())}")
    print(f"是否包含function_description: {'function_description' in serialized_data}")
    
    if 'function_description' in serialized_data:
        print(f"function_description值: '{serialized_data['function_description']}'")
    else:
        print("不包含function_description字段")
        # 手动添加
        serialized_data['function_description'] = instance.function_description
        print(f"手动添加后的值: '{serialized_data['function_description']}'")

# 测试多个实例
print("\n--- 测试多个实例 ---")

instances = EquipmentInstance.objects.all()[:3]
serializer = EquipmentInstanceSerializer(instances, many=True)
serialized_data = serializer.data

for i, data in enumerate(serialized_data, 1):
    print(f"\n第{i}个实例序列化后的数据字段: {sorted(data.keys())}")
    print(f"是否包含function_description: {'function_description' in data}")
    if 'function_description' in data:
        print(f"function_description值: '{data['function_description']}'")
    else:
        print("不包含function_description字段")