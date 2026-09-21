#!/usr/bin/env python3
"""
测试新的API端点
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


def test_new_endpoint():
    """测试新的API端点"""
    print("测试新的API端点...\n")
    
    # 创建API客户端
    client = APIClient()
    
    # 强制认证为管理员用户
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        client.force_authenticate(user=admin_user)
        print(f"已强制认证为管理员用户: {admin_user.username}")
    
    # 测试新的API端点
    url = '/api/test-equipment-instances/'
    print(f"\n测试API端点: {url}")
    
    try:
        # 发送GET请求
        response = client.get(url)
        
        # 检查响应状态码
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == status.HTTP_200_OK:
            # 检查响应数据
            data = response.data
            print(f"响应包含results: {'results' in data}")
            print(f"响应包含count: {'count' in data}")
            
            if 'results' in data:
                results = data['results']
                print(f"结果数量: {len(results)}")
                
                if results:
                    # 检查每个结果
                    for i, item in enumerate(results[:3], 1):
                        print(f"\n第{i}个结果包含字段: {sorted(item.keys())}")
                        if 'function_description' in item:
                            fd_value = item['function_description']
                            print(f"  function_description: '{fd_value}'")
                        else:
                            print("  缺少function_description字段")
        else:
            print(f"API请求失败，响应内容: {response.data}")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_new_endpoint()