#!/usr/bin/env python3
"""
使用Django shell测试API响应
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
from equipment.models import EquipmentInstance


def test_api_response():
    """使用Django shell测试API响应"""
    print("使用Django shell测试API响应...\n")
    
    # 创建API客户端
    client = APIClient()
    
    # 获取测试用户
    User = get_user_model()
    try:
        # 使用第一个用户（假设是管理员）
        user = User.objects.first()
        if user:
            client.force_authenticate(user=user)
            print(f"已使用用户: {user.username}")
        else:
            print("没有找到用户，使用匿名用户")
    except Exception as e:
        print(f"获取用户失败: {e}")
    
    # API端点URL
    url = "/api/equipment/instances/"
    
    try:
        # 发送GET请求
        response = client.get(url)
        
        # 检查响应状态码
        if response.status_code == status.HTTP_200_OK:
            # 解析响应JSON
            data = response.json()
            
            print(f"\nAPI响应状态码: {response.status_code}")
            print("API响应结构:")
            print(f"- 包含results: {'results' in data}")
            print(f"- 包含count: {'count' in data}")
            
            if 'results' in data:
                instances = data['results']
                print(f"\n设备实例数量: {len(instances)}")
                
                if instances:
                    print(f"\n第一个设备实例数据结构:")
                    import json
                    print(json.dumps(instances[0], indent=2, ensure_ascii=False))
                    
                    print(f"\n第一个设备实例包含的字段:")
                    for key in sorted(instances[0].keys()):
                        value = instances[0][key]
                        value_type = type(value).__name__
                        print(f"- {key}: {value} ({value_type})")
                    
                    print(f"\n第一个设备实例功能描述字段:")
                    if 'function_description' in instances[0]:
                        fd = instances[0]['function_description']
                        print(f"  - 值: '{fd}'")
                        print(f"  - 类型: {type(fd).__name__}")
                        print(f"  - 长度: {len(fd) if fd else 0}")
                        print(f"  - 是否为空: {not fd}")
                    else:
                        print("  - 功能描述字段不存在")
        else:
            print(f"API请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.data}")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_api_response()