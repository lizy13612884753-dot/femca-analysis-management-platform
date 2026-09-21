#!/usr/bin/env python3
"""
测试更新设备实例的功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
import django
django.setup()

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


def test_update_equipment_instance():
    """测试更新设备实例"""
    print("测试更新设备实例...")
    
    # 创建API客户端
    client = APIClient()
    
    # 强制认证为管理员用户
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        client.force_authenticate(user=admin_user)
        print(f"已强制认证为管理员用户: {admin_user.username}")
    else:
        # 尝试使用第一个用户
        first_user = User.objects.first()
        if first_user:
            client.force_authenticate(user=first_user)
            print(f"已强制认证为用户: {first_user.username}")
        else:
            print("没有找到用户，无法测试")
            return
    
    # 先获取设备实例的信息
    instance_url = '/api/equipment/instances/1/'
    response = client.get(instance_url)
    if response.status_code != status.HTTP_200_OK:
        print(f"获取设备实例失败，状态码: {response.status_code}")
        return
    
    instance_data = response.data
    print(f"设备实例当前数据: {instance_data}")
    
    # 测试更新设备实例
    url = instance_url
    print(f"\n测试API端点: {url}")
    
    # 准备更新数据（只更新function_description和name字段）
    update_data = {
        'name': '测试设备更新',
        'function_description': '测试更新的功能描述',
        'equipment_type': instance_data.get('equipment_type'),
        'serial_number': instance_data.get('serial_number')
    }
    
    try:
        # 发送PUT请求
        response = client.put(url, update_data)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == status.HTTP_200_OK:
            print("更新成功！")
            print(f"响应数据: {response.data}")
        else:
            print("更新失败！")
            print(f"响应内容: {response.content}")
            print(f"响应状态码: {response.status_code}")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_update_equipment_instance()
