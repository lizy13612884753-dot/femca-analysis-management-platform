#!/usr/bin/env python3
"""
使用DRF的测试客户端测试完整的API响应
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


def test_api_with_drf_client():
    """使用DRF的测试客户端测试完整的API响应"""
    print("使用DRF的测试客户端测试完整的API响应...\n")
    
    # 创建API客户端
    client = APIClient()
    
    # 强制认证为管理员用户
    from django.contrib.auth import get_user_model
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
    
    # 测试设备实例列表API
    url = '/api/equipment/instances/'
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
                    # 打印第一个结果的完整内容
                    print(f"\n第一个结果的完整内容: {results[0]}")
                    
                    # 检查前3个结果
                    for i, item in enumerate(results[:3], 1):
                        print(f"\n第{i}个结果包含字段: {sorted(item.keys())}")
                        if 'function_description' in item:
                            fd_value = item['function_description']
                            print(f"  function_description: '{fd_value}'")
                        else:
                            print("  缺少function_description字段")
                            # 尝试直接访问字段
                            try:
                                print(f"  直接访问function_description: {item.function_description}")
                            except AttributeError:
                                print(f"  直接访问失败")
                            # 打印item的类型
                            print(f"  item类型: {type(item)}")
        else:
            print(f"API请求失败，响应内容: {response.data}")
            
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_new_endpoint_with_drf_client():
    """测试新创建的端点"""
    print("\n=== 测试新端点 ===")
    print("使用DRF的测试客户端测试新端点...\n")
    
    # 创建API客户端
    client = APIClient()
    
    # 强制认证为管理员用户
    from django.contrib.auth import get_user_model
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
    
    # 测试新创建的端点
    url = '/api/equipment/instances/test-function-description/'
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
                    # 检查所有结果
                    for i, item in enumerate(results, 1):
                        print(f"\n第{i}个结果: {item}")
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
    test_api_with_drf_client()
    test_new_endpoint_with_drf_client()