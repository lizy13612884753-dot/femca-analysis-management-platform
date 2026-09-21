#!/usr/bin/env python3
"""
直接测试视图集的list方法，查看详细的调试输出
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'femca_platform.settings')
import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from equipment.views import EquipmentInstanceViewSet


def test_list_view_debug():
    """直接测试视图集的list方法，查看详细的调试输出"""
    print("直接测试视图集的list方法，查看详细的调试输出...\n")
    
    # 创建请求工厂
    factory = RequestFactory()
    
    # 创建GET请求
    request = factory.get('/api/equipment/instances/')
    
    # 获取测试用户
    User = get_user_model()
    try:
        # 使用第一个用户（假设是管理员）
        user = User.objects.first()
        if user:
            request.user = user
            print(f"已使用用户: {user.username}")
        else:
            print("没有找到用户，使用匿名用户")
    except Exception as e:
        print(f"获取用户失败: {e}")
    
    # 创建视图集实例
    view = EquipmentInstanceViewSet.as_view({'get': 'list'})
    
    try:
        # 调用视图方法
        response = view(request)
        
        # 检查响应状态码
        print(f"\n响应状态码: {response.status_code}")
        
        # 检查响应数据
        if hasattr(response, 'data'):
            data = response.data
            print(f"响应数据包含results: {'results' in data}")
            
            if 'results' in data:
                results = data['results']
                print(f"结果数量: {len(results)}")
                
                if results:
                    first_item = results[0]
                    print(f"第一个结果包含字段: {sorted(first_item.keys())}")
                    if 'function_description' in first_item:
                        print(f"function_description值: '{first_item['function_description']}'")
                    else:
                        print("第一个结果不包含function_description字段")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_list_view_debug()