#!/usr/bin/env python3
"""
直接检查序列化器的配置
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
import django
django.setup()

from equipment.serializers import EquipmentInstanceListSerializer
from equipment.models import EquipmentInstance


def check_serializer_config():
    """直接检查序列化器的配置"""
    print("直接检查序列化器的配置...\n")
    
    # 创建序列化器实例
    serializer = EquipmentInstanceListSerializer()
    
    print(f"序列化器类名: {serializer.__class__.__name__}")
    print(f"序列化器字段: {sorted(serializer.fields.keys())}")
    print(f"是否包含function_description字段: {'function_description' in serializer.fields}")
    
    if 'function_description' in serializer.fields:
        fd_field = serializer.fields['function_description']
        print(f"\nfunction_description字段类型: {fd_field.__class__.__name__}")
        print(f"是否为只读: {fd_field.read_only}")
        print(f"是否需要: {fd_field.required}")
    
    print("\n检查模型字段...")
    from equipment.models import EquipmentInstance
    model_fields = [f.name for f in EquipmentInstance._meta.fields]
    print(f"模型包含的字段: {sorted(model_fields)}")
    print(f"模型是否包含function_description字段: {'function_description' in model_fields}")
    
    # 获取一个设备实例
    instance = EquipmentInstance.objects.first()
    if instance:
        print(f"\n获取第一个设备实例: ID={instance.id}, 名称={instance.name}")
        print(f"设备实例的function_description值: '{instance.function_description}'")
        print(f"设备实例的function_description长度: {len(instance.function_description) if instance.function_description else 0}")
        
        # 测试序列化器序列化数据
        print("\n测试序列化器序列化数据...")
        serialized_data = serializer.to_representation(instance)
        print(f"序列化后的数据包含字段: {sorted(serialized_data.keys())}")
        print(f"序列化后的数据是否包含function_description: {'function_description' in serialized_data}")
        if 'function_description' in serialized_data:
            print(f"序列化后的function_description值: '{serialized_data['function_description']}'")
        else:
            print("序列化后的数据不包含function_description字段")
            print(f"序列化后的数据内容: {serialized_data}")
    else:
        print("\n没有找到设备实例")


if __name__ == "__main__":
    check_serializer_config()