#!/usr/bin/env python3
"""
测试前端API返回的数据结构
"""

import requests
import json

def test_api_response():
    """测试前端API返回的数据结构"""
    print("测试前端API返回的数据结构...\n")
    
    # API端点URL
    url = "http://localhost:8000/api/equipment/instances/"
    
    try:
        # 发送GET请求
        response = requests.get(url)
        
        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应JSON
            data = response.json()
            
            print("API响应结构:")
            print(f"- 包含results: {'results' in data}")
            print(f"- 包含count: {'count' in data}")
            
            if 'results' in data:
                instances = data['results']
                print(f"\n设备实例数量: {len(instances)}")
                
                if instances:
                    print(f"\n第一个设备实例数据结构:")
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
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    test_api_response()