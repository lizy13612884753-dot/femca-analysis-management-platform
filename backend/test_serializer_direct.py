#!/usr/bin/env python3
"""
直接测试序列化器，不通过完整的API请求流程
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
from equipment.serializers import EquipmentInstanceListSerializer


def test_serializer_direct():
    """直接测试序列化器"""
    print("直接测试序列化器，不通过完整的API请求流程...\n")
    
    # 获取所有设备实例
    instances = EquipmentInstance.objects.all()
    print(f"设备实例总数: {instances.count()}\n")
    
    if not instances:
        print("没有设备实例，无法测试")
        return
    
    # 先单独测试一个序列化器实例，了解字段配置
    print("测试单个序列化器实例:")
    single_serializer = EquipmentInstanceListSerializer(instance=instances.first())
    print(f"序列化器类名: {single_serializer.__class__.__name__}")
    print(f"序列化器字段: {sorted(single_serializer.fields.keys())}")
    print(f"是否包含function_description字段: {'function_description' in single_serializer.fields}")
    
    # 再测试多个实例的序列化
    print("\n测试多个实例的序列化:")
    many_serializer = EquipmentInstanceListSerializer(instance=instances, many=True)
    
    # 获取序列化后的数据
    serialized_data = many_serializer.data
    print(f"\n序列化后的数据数量: {len(serialized_data)}")
    
    if serialized_data:
        # 检查每个序列化后的数据项
        for i, item in enumerate(serialized_data[:3], 1):  # 只检查前3个
            print(f"\n第{i}个序列化数据项包含字段: {sorted(item.keys())}")
            if 'function_description' in item:
                fd_value = item['function_description']
                print(f"  function_description值: '{fd_value}'")
                print(f"  function_description长度: {len(fd_value) if fd_value else 0}")
                print(f"  function_description类型: {type(fd_value).__name__}")
            else:
                print("  不包含function_description字段")
    
    # 对比数据库中的数据
    print("\n对比数据库中的数据...")
    for i, instance in enumerate(instances[:3], 1):  # 只检查前3个
        print(f"\n第{i}个数据库实例:")
        print(f"  ID: {instance.id}")
        print(f"  名称: {instance.name}")
        print(f"  function_description: '{instance.function_description}'")
        print(f"  长度: {len(instance.function_description) if instance.function_description else 0}")
        print(f"  类型: {type(instance.function_description).__name__}")


if __name__ == "__main__":
    test_serializer_direct()